import subprocess
import sys
import os

# --- 配置 ---
# 默认的远程仓库和分支名
REMOTE = 'origin'
BRANCH = 'main' # 请根据你的仓库实际情况修改为 'master' 或 'main'

def run_command(command, print_output=True, check_error=True):
    """
    执行一个给定的 Shell 命令，并返回执行结果。

    :param command: 包含命令和参数的列表，例如 ['git', 'status']
    :param print_output: 是否在终端打印命令的输出。
    :param check_error: 如果命令执行失败（非零退出代码），是否抛出异常。
    :return: subprocess.CompletedProcess 对象
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True, # 捕获输出
            text=True,           # 解码为字符串
            check=check_error    # 检查错误码
        )

        if print_output and result.stdout:
            print(f"--- 结果: {' '.join(command)} ---")
            print(result.stdout.strip())
        
        return result

    except subprocess.CalledProcessError as e:
        print(f"\n[❌ 错误] 命令执行失败: {' '.join(command)}", file=sys.stderr)
        print(f"退出代码: {e.returncode}", file=sys.stderr)
        print(f"标准错误: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1) # 发现错误后退出脚本
    except FileNotFoundError:
        print("错误：系统中找不到 Git 命令。请确认 Git 已安装。", file=sys.stderr)
        sys.exit(1)

def git_autopush(commit_message):
    """
    执行 Git 流程：状态检查 -> git add . -> git commit -> git push
    """
    print(f"--- 🚀 正在执行 Git 自动推送流程 ---")

    # 1. 检查当前目录是否是一个 Git 仓库
    try:
        run_command(['git', 'rev-parse', '--is-inside-work-tree'], print_output=False)
        print("✅ 检查通过：当前目录是一个 Git 仓库。")
    except subprocess.CalledProcessError:
        print("[❌ 致命错误] 当前目录不是一个 Git 仓库。请先执行 git init。", file=sys.stderr)
        sys.exit(1)
        
    # 2. 检查当前分支名
    current_branch_result = run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], print_output=False, check_error=True)
    current_branch = current_branch_result.stdout.strip()
    print(f"📌 当前分支: {current_branch}")

    # 3. 检查状态（可选，用于展示）
    run_command(['git', 'status', '-s'])

    # 4. git add . (添加所有更改到暂存区)
    print("\n--- ➕ 正在添加所有更改 (git add .) ---")
    run_command(['git', 'add', '.'], print_output=False)
    print("✅ 所有更改已添加到暂存区。")

    # 5. git commit (提交更改)
    print(f"\n--- 📝 正在提交更改 (git commit -m '{commit_message}') ---")
    # 注意：如果没有任何更改，commit 会失败，这里我们不使用 check=True，而是手动检查 stderr
    commit_result = run_command(['git', 'commit', '-m', commit_message], print_output=True, check_error=False) 
    
    if commit_result.returncode != 0:
        if "nothing to commit" in commit_result.stderr:
             print("⚠️ 警告：自上次提交后，工作区没有新的更改。跳过提交步骤。")
        else:
            print(f"[❌ 错误] 提交失败，错误信息:\n{commit_result.stderr}", file=sys.stderr)
            sys.exit(1)

    # 6. git push (推送到远程仓库)
    print(f"\n--- 📤 正在推送到远程仓库 ({REMOTE}/{BRANCH}) ---")
    run_command(['git', 'push', REMOTE, current_branch]) # 使用实际分支名推送

    print("\n--- 🎉 推送成功！Git 自动化流程完成。 ---")

if __name__ == "__main__":
    # 在命令行中运行脚本时，可以提供提交信息作为参数
    # 例如： python3 git_autopush.py "Feat: 完成了新的登录模块"
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    else:
        commit_msg = "Auto commit: Updated files" # 默认提交信息

    git_autopush(commit_msg)
