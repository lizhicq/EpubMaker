import os, wave
import edge_tts
import asyncio
from tqdm import tqdm
import signal

class Task:
    def __init__(self, name, text, output_file):
        self.name = name
        self.text = text
        self.output_file = output_file

class TxtToWavConverter:
    def __init__(self, input_dir, output_dir, voice="zh-CN-XiaoxiaoNeural", max_concurrency=100, task_timeout=120, total_timeout=600):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.voice = voice
        self.max_concurrency = max_concurrency
        self.task_timeout = task_timeout
        self.total_timeout = total_timeout

    async def text_to_speech(self, task):
        try:
            communicate = edge_tts.Communicate(task.text, self.voice)
            await asyncio.wait_for(communicate.save(task.output_file), timeout=self.task_timeout)
            return True
        except asyncio.TimeoutError as e:
            print(f"Timeout Error processing {task.output_file}: {e}")
            return task
        except Exception as e:
            print(f"Other Error processing {task.output_file}: {e}")
            return task

    async def process_tasks(self, tasks):
        print(f"process {len(tasks)} tasks {[task.name for task in tasks]}")
        semaphore = asyncio.Semaphore(self.max_concurrency)
        async def limited_task(task):
            async with semaphore:
                return await self.text_to_speech(task)
        async def inner():
            return [await future for future in tqdm(
                asyncio.as_completed([limited_task(task) for task in tasks]),
                total=len(tasks), desc="Processing")]
        try:
            # 将总超时逻辑移入此处
            return await asyncio.wait_for(inner(), timeout=self.total_timeout)
        except asyncio.TimeoutError:
            print("Total processing timeout reached. Exiting process_tasks.")
            return None

    def is_file_size_valid(self, txt_file_path, wav_file_path, min_size_ratio=5.9/16):
        try:
            txt_size_kb = os.path.getsize(txt_file_path) / 1024
            wav_size_mb = os.path.getsize(wav_file_path) / (1024 * 1024)
            return wav_size_mb >= 0.9 * txt_size_kb * min_size_ratio
        except FileNotFoundError:
            return False

    async def process_txt_files(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        tasks = []
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".txt"):
                txt_path = os.path.join(self.input_dir, filename)
                wav_path = os.path.join(self.output_dir, filename.replace(".txt", ".wav"))
                if not (os.path.exists(wav_path) and self.is_file_size_valid(txt_path, wav_path)):
                    with open(txt_path, "r", encoding="utf-8") as f:
                        text = f.read().strip()
                    if text:
                        tasks.append(Task(filename, text, wav_path))
        return tasks

    def timeout_handler(self, signum, frame):
        raise TimeoutError("Processing time exceeded")

    async def run(self):
        for attempt in range(10):
            tasks = await self.process_txt_files()
            results = await self.process_tasks(tasks)
            if results is None:
                print("Skipping current attempt due to total timeout.")
                continue
            if all(result is True for result in results):
                print("No unfinished txts needing to be converted, exit")
                break
            print(f"\nSome tasks failed. Retrying...")
            self.task_timeout += 20
            success_count = results.count(True)
            undone_count = len(results) - success_count
            print(f"\nAttempt {attempt + 1} completed! Success: {success_count}, unfinished: {undone_count}")
        print("All done or reached max attempts!")

if __name__ == "__main__":
    novel = "武极天下"
    input_directory = f"/Users/lizhicq/GitHub/EpubMaker/data/txt/{novel}"
    output_directory = f"/Users/lizhicq/GitHub/EpubMaker/data/audio/{novel}"
    voice = "zh-CN-YunxiNeural"
    converter = TxtToWavConverter(input_directory, output_directory, voice)
    asyncio.run(converter.run())