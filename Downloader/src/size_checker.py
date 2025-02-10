import os, wave


def check_dir_size(input_dir):
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not is_wav_file_playable(fp):
                print(f"File {f} is not playable...")

def is_wav_file_playable(file_path):
    """
    检查 .wav 文件是否可以播放
    """
    try:
        with wave.open(file_path, 'rb') as wav_file:
            # 尝试读取文件的基本信息
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            # 如果文件没有帧或采样率，则认为不可播放
            if frames == 0 or rate == 0:
                return False
        return True
    except (wave.Error, EOFError):
        # 如果文件无法打开或格式错误，则认为不可播放
        return 

if __name__ == "__main__":
    check_dir_size('data/audio/神级大魔头')