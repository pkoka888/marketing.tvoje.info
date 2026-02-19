# Parallel Orchestration Results

## Agent: kilo

Status: Failure Duration: 1.80s

### Output

```
kilo run [message..]

run kilo with a message

Positionals:
  message  message to send                                                     [array] [default: []]

Options:
  -h, --help        show help                                                              [boolean]
  -v, --version     show version number                                                    [boolean]
      --print-logs  print logs to stderr                                                   [boolean]
      --log-level   log level                   [string] [choices: "DEBUG", "INFO", "WARN", "ERROR"]
      --command     the command to run, use message for args                                [string]
  -c, --continue    continue the last session                                              [boolean]
  -s, --session     session id to continue                                                  [string]
      --fork        fork the session before continuing (requires --continue or --session)  [boolean]
      --share       share the session                                                      [boolean]
  -m, --model       model to use in the format of provider/model                            [string]
      --agent       agent to use                                                            [string]
      --format      format: default (formatted) or json (raw JSON events)
                                          [string] [choices: "default", "json"] [default: "default"]
  -f, --file        file(s) to attach to message                                             [array]
      --title       title for the session (uses truncated prompt if no value provided)      [string]
      --attach      attach to a running opencode server (e.g., http://localhost:4096)       [string]
      --port        port for the local server (defaults to random port if no value provided)[number]
      --variant     model variant (provider-specific reasoning effort, e.g., high, max, minimal)
                                                                                            [string]
      --thinking    show thinking blocks                                  [boolean] [default: false]
      --auto        auto-approve all permissions (for autonomous/pipeline usage)
                                                                          [boolean] [default: false]

```

## Agent: cline

Status: Failure Duration: 53.18s

### Output

```
{"message":"402 Insufficient balance. Your Cline Credits balance is $0.01","status":402,"code":"insufficient_credits","modelId":"minimax/minimax-m2.1","providerId":"cline","details":{"code":"insufficient_credits","message":"Insufficient balance. Your Cline Credits balance is $0.01","current_balance":0.009608,"total_spent":0,"total_promotions":0,"buy_credits_url":"https://app.cline.bot/credits"}}

```

### Error

```
Task started: 1771463273774
Error: API request failed: {"message":"402 Insufficient balance. Your Cline Credits balance is $0.01","status":402,"code":"insufficient_credits","modelId":"minimax/minimax-m2.1","providerId":"cline","details":{"code":"insufficient_credits","message":"Insufficient balance. Your Cline Credits balance is $0.01","current_balance":0.009608,"total_spent":0,"total_promotions":0,"buy_credits_url":"https://app.cline.bot/credits"}}
Error: {"message":"402 Insufficient balance. Your Cline Credits balance is $0.01","status":402,"code":"insufficient_credits","modelId":"minimax/minimax-m2.1","providerId":"cline","details":{"code":"insufficient_credits","message":"Insufficient balance. Your Cline Credits balance is $0.01","current_balance":0.009608,"total_spent":0,"total_promotions":0,"buy_credits_url":"https://app.cline.bot/credits"}}

```
