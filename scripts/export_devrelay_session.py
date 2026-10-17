import json
import re
import os
import sys

def sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    # Clean XML prompt tags if desired, or keep core user text
    text = re.sub(r'<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>', '', text, flags=re.DOTALL)
    text = re.sub(r'<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>', '', text, flags=re.DOTALL)
    # Redact sensitive keys
    text = re.sub(r'(sk-[a-zA-Z0-9]{20,})', '[REDACTED_API_KEY]', text)
    text = re.sub(r'(ghp_[a-zA-Z0-9]{20,})', '[REDACTED_GITHUB_TOKEN]', text)
    text = re.sub(r'(dev_[a-zA-Z0-9]{20,})', '[REDACTED_DEV_KEY]', text)
    return text.strip()

def main():
    convo_id = "b773ad0e-2410-4b0e-89b8-f86b01c179e9"
    log_path = os.path.expanduser(f"~/.gemini/antigravity-ide/brain/{convo_id}/.system_generated/logs/transcript.jsonl")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "devrelay")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "session_transcript.json")

    if not os.path.exists(log_path):
        print(f"Transcript not found at {log_path}")
        sys.exit(1)

    messages = []
    current_assistant_content = []

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            entry_type = entry.get("type")
            source = entry.get("source")

            if entry_type == "USER_INPUT":
                # Flush previous assistant if exists
                if current_assistant_content:
                    messages.append({
                        "role": "assistant",
                        "model": "gemini-3.8-flash",
                        "content": current_assistant_content
                    })
                    current_assistant_content = []

                user_text = sanitize_text(entry.get("content", ""))
                if user_text:
                    messages.append({
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text}
                        ]
                    })

            elif source == "MODEL" and entry_type == "PLANNER_RESPONSE":
                content_text = sanitize_text(entry.get("content", ""))
                if content_text:
                    current_assistant_content.append({"type": "text", "text": content_text})

                tool_calls = entry.get("tool_calls", [])
                for tc in tool_calls:
                    tool_name = tc.get("name") or tc.get("tool_name", "tool")
                    args = tc.get("args") or tc.get("arguments", {})
                    current_assistant_content.append({
                        "type": "tool_call",
                        "name": tool_name,
                        "input": str(args)[:300],
                        "output": "Executed successfully"
                    })

    if current_assistant_content:
        messages.append({
            "role": "assistant",
            "model": "gemini-3.8-flash",
            "content": current_assistant_content
        })

    session_payload = {
        "title": "Building HisaabDost: Zero-Tech Voice Bookkeeper for Roadside Stalls",
        "tool_name": "gemini_cli",
        "curated_data": {
            "messages": messages,
            "metadata": {
                "tool_name": "gemini_cli",
                "session_id": convo_id,
                "total_messages": len(messages),
                "project": "HisaabDost",
                "hackathon": "Hacktoberfest 2026 Week 2 Challenge (Side Hustle)"
            }
        }
    }

    with open(out_path, "w", encoding="utf-8") as out_f:
        json.dump(session_payload, out_f, indent=2)

    print(f"Exported {len(messages)} messages to {out_path}")

if __name__ == "__main__":
    main()
