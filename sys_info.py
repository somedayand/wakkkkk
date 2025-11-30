import subprocess
import sys

# 脚本目标：执行 Linux 命令 'ls -lh' 并捕获输出

def run_linux_command(command_list):
    """
    执行一个给定的 Linux 命令列表，并处理其输出和错误。

    :param command_list: 一个包含命令及其参数的列表，例如 ['ls', '-lh']
    :return: None
    """
    print(f"--- 正在执行命令: {' '.join(command_list)} ---")

    try:
        # 使用 subprocess.run() 执行命令
        result = subprocess.run(
            command_list,        # 要执行的命令和参数
            capture_output=True, # 捕获标准输出和标准错误
            text=True,           # 将输出和错误解码为文本（字符串），而不是字节
            check=True           # 如果命令返回非零退出代码（即命令失败），则抛出 CalledProcessError 异常
        )

        # 打印命令的标准输出
        print("\n--- 命令输出 ---")
        print(result.stdout.strip())
        print("------------------\n")

    except subprocess.CalledProcessError as e:
        # 捕获由于 check=True 导致的命令执行失败
        print(f"错误：命令执行失败，退出代码 {e.returncode}", file=sys.stderr)
        print(f"错误信息：{e.stderr.strip()}", file=sys.stderr)
    except FileNotFoundError:
        # 捕获命令本身不存在的错误（例如，系统中没有'ls'这个命令）
        print(f"错误：找不到命令 '{command_list[0]}'", file=sys.stderr)
    except Exception as e:
        # 捕获其他未知异常
        print(f"发生未知错误: {e}", file=sys.stderr)


if __name__ == "__main__":
    # 定义要执行的命令及其参数
    target_command = ['ls', '-lh']
    
    # 调用函数执行命令
    run_linux_command(target_command)

    # 示例：执行一个带有参数的命令 (例如，查看 /home 目录)
    # run_linux_command(['ls', '-lh', '/home'])
    
    # 示例：执行一个错误命令 (例如，ls -invalid_arg)
    # run_linux_command(['ls', '-invalid_arg'])
