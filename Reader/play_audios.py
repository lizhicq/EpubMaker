import subprocess
import os
import librosa  # 导入 librosa 库


def get_play_list(audio_dir):
    """
    获取音频文件列表

    参数:
    audio_dir (str): 音频文件所在目录的完整路径

    返回:
    list: 音频文件列表
    """
    # 检查目录是否存在
    if not os.path.exists(audio_dir):
        raise FileNotFoundError(f"目录 {audio_dir} 不存在")

    # 获取目录下的所有文件
    files = os.listdir(audio_dir)

    # 过滤出音频文件
    audio_files = [f for f in files if f.endswith(('.mp3', '.wav', '.m4a'))]
    audio_files.sort(key=lambda x: int(x.split('-')[0]))  # 按文件名排序
    return audio_files

def play_with_nplayer(file_path, speed=2.0):
    """
    使用 nPlayer 播放音频文件并设置播放速度，并根据音频时长动态设置延迟时间

    参数:
    file_path (str): 音频文件的完整路径
    speed (float): 播放速度倍数
    """
    # 确保文件路径是绝对路径
    abs_path = os.path.abspath(file_path)

    try:
        # 使用 librosa 获取音频文件的时长 (单位为秒)
        duration = librosa.get_duration(filename=abs_path)
        # 为了确保 nPlayer 有足够的时间加载和开始播放，
        # 我们可以将 time_delay 设置为略大于音频时长的值，例如加上 2 秒的缓冲
        time_delay = int(duration/speed) + 2  # 转换为整数秒，并增加缓冲时间
        print(f"音频{file_path.split('/')[-1]}时长为 {duration:.2f} 秒，设置 time_delay 为 {time_delay} 秒") # 打印时长信息
    except Exception as e:
        print(f"获取音频时长失败: {str(e)}, 使用默认 time_delay = 5 秒")
        time_delay = 5  # 如果获取时长失败，则使用默认值

    # 构建 AppleScript 命令，与之前的代码基本相同
    applescript = f'''
        tell application "nPlayer"
            open "{abs_path}"
        end tell

        tell application "System Events"
            activate application "nPlayer" -- 确保 nPlayer 处于激活状态

            tell process "nPlayer"
                -- 循环点击子菜单的第一个菜单项 10 次 (降低播放速度)
                repeat 10 times
                    click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
                end repeat

            end tell
        end tell

        delay {time_delay}

        -- 关闭 nPlayer 应用程序 (精简版本)
        tell application "nPlayer"
            quit
        end tell
    '''

    try:
        # 执行 AppleScript
        subprocess.run(['osascript', '-e', applescript])
        print(f"正在使用 nPlayer 以 {speed}x 速度播放")

    except Exception as e:
        print(f"调用 nPlayer 时出错: {str(e)}")

if __name__ == "__main__":
    audio_dir = "/Users/lizhicq/GitHub/EpubMaker/data/audio/神级大魔头"  # 替换为你的音频文件目录
    audio_files = get_play_list(audio_dir)
    for file in audio_files[920:]:
        file_path = os.path.join(audio_dir, file)
        play_with_nplayer(file_path, speed=2.0)  # 播放速度设置为 2.0x