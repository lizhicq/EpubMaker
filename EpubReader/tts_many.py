import os
import edge_tts
import asyncio
from tqdm import tqdm

async def text_to_speech(text, output_file, voice="zh-CN-XiaoxiaoNeural"):
    """使用 Edge TTS 将文本转换为语音"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return True  # 成功标志
    except Exception as e:
        print(f"Error processing {output_file}: {e}")
        return (output_file, text)  # 返回失败的任务信息

async def process_tasks(tasks, max_concurrency=10):
    """并发处理任务"""
    semaphore = asyncio.Semaphore(max_concurrency)  # 控制最大并发数

    async def limited_task(task):
        async with semaphore:
            return await task

    # 使用 tqdm 显示进度条
    results = []
    for future in tqdm(asyncio.as_completed([limited_task(task) for task in tasks]), total=len(tasks), desc="Processing"):
        results.append(await future)
    return results

async def process_txt_files(input_dir, output_dir, voice="zh-CN-XiaoxiaoNeural"):
    """遍历输入目录中的所有 .txt 文件，并生成任务列表"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tasks = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            txt_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename.replace(".txt", ".wav"))

            with open(txt_file_path, "r", encoding="utf-8") as file:
                text = file.read()

            # 创建任务
            task = text_to_speech(text, output_file_path, voice)
            tasks.append(task)

    return tasks

async def retry_failed_tasks(failed_tasks, max_retries=3):
    """重试失败的任务"""
    for attempt in range(max_retries):
        print(f"\nRetrying failed tasks (Attempt {attempt + 1})...")
        
        # 将失败的任务重新转换为异步任务
        retry_tasks = [text_to_speech(text, output_file) for (output_file, text) in failed_tasks]
        
        # 处理重试任务
        retry_results = await process_tasks(retry_tasks)
        
        # 收集新的失败任务
        failed_tasks = [task for task in retry_results if task is not True]
        
        if not failed_tasks:  # 如果没有失败任务，退出重试
            break
    
    return failed_tasks

async def main():
    input_directory = "data/txt/大奉打更人"  # 替换为你的 txt 文件目录
    output_directory = "data/audio/大奉打更人-男声"  # 替换为你想保存音频文件的目录
    voice = "zh-CN-YunxiNeural"  # 选择语音

    # 获取任务列表
    tasks = await process_txt_files(input_directory, output_directory, voice)

    # 并发处理任务
    results = await process_tasks(tasks, max_concurrency=300)  # 设置最大并发数

    # 收集失败的任务
    failed_tasks = [task for task in results if task is not True]

    # 如果有失败的任务，进行重试
    if failed_tasks:
        print(f"\n{len(failed_tasks)} tasks failed. Retrying...")
        failed_tasks = await retry_failed_tasks(failed_tasks)

    # 统计成功和失败的任务数
    success_count = results.count(True) + (len(failed_tasks) - len([task for task in failed_tasks if task is not True]))
    failure_count = len(failed_tasks)
    print(f"\nProcessing complete! Success: {success_count}, Failed: {failure_count}")

if __name__ == "__main__":
    asyncio.run(main())