import subprocess

def get_git_log():
    log_cmd = [
        "git", "log",
        "--pretty=format:=== Commit: %h ===%nAuthor: %an%nDate: %ad%nMessage: %s%n",
        "--date=short",
        "--numstat"
    ]
    result = subprocess.run(log_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def format_log(raw_log):
    lines = raw_log.strip().split('\n')
    output = []
    for line in lines:
        if line.startswith("==="):  # commit delimiter
            output.append("\n" + line)
        elif line.strip() == "":
            continue
        elif "\t" in line:  # file change line from numstat
            added, deleted, filename = line.split("\t")
            output.append(f"  • {filename} (+{added} / -{deleted})")
        else:
            output.append(line)
    return "\n".join(output)

def save_log_to_txt(formatted_log, filename="git_log.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(formatted_log)
    print(f"✅ Git log has been saved to {filename}")

if __name__ == "__main__":
    raw_log = get_git_log()
    formatted = format_log(raw_log)
    save_log_to_txt(formatted)
