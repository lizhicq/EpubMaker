import os, wave
import edge_tts
import asyncio
from tqdm import tqdm


async def text_to_speech(text, output_file, voice="zh-CN-XiaoxiaoNeural"):
    """使用 Edge TTS 将文本转换为语音"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await asyncio.wait_for(communicate.save(output_file), timeout=120)
        return True  # 成功标志
    except asyncio.TimeoutError:
        print(f"Timeout processing {output_file}")
        return (output_file, text)  # 返回失败的任务信息
    except Exception as e:
        print(f"Error processing {output_file}: {e}")
        return (output_file, text)  # 返回失败的任务信息

async def process_tasks(tasks, max_concurrency=100):
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

def is_wav_playable(file_path):
    """检查 .wav 文件是否可以播放（同步函数）"""
    try:
        with wave.open(file_path, 'rb') as wav:
            if wav.getnframes() > 0 and wav.getframerate() > 0:
                return True
        return False
    except (wave.Error, EOFError, FileNotFoundError):
        return False

async def process_txt_files(input_dir, output_dir, voice="zh-CN-XiaoxiaoNeural"):
    """处理需要生成的文本文件，跳过已存在且可播放的 .wav 文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tasks = []
    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue

        # 构建输入/输出路径
        txt_path = os.path.join(input_dir, filename)
        wav_filename = filename.replace(".txt", ".wav")
        wav_path = os.path.join(output_dir, wav_filename)

        # 检查目标文件是否需要处理
        need_process = True
        if os.path.exists(wav_path):
            if is_wav_playable(wav_path):  # 如果能播放则跳过
                print(f"Skipped: {wav_path} (already playable)")
                need_process = False

        # 需要处理时创建任务
        if need_process:
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            
            if text:  # 避免处理空文本
                task = text_to_speech(text, wav_path, voice)
                tasks.append(task)
            else:
                print(f"Skipped: {txt_path} (empty content)")

    return tasks

async def retry_failed_tasks(failed_tasks, max_retries=10):
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
    novel = "神级大魔头"
    input_directory = f"/Users/lizhicq/GitHub/EpubMaker/data/txt/{novel}"  # 替换为你的 txt 文件目录
    output_directory = f"/Users/lizhicq/GitHub/EpubMaker/data/audio/{novel}"  # 替换为你想保存音频文件的目录
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