#!/usr/bin/env bash
# smoke_test.sh — testa todos os subjects NATS do prompt-ver-core
# Requer: nats CLI instalado (https://github.com/nats-io/natscli)

set -euo pipefail

NATS_URL="${NATS_URL:-nats://localhost:4222}"
PASS=0
FAIL=0

RESP_FILE=$(mktemp)
trap 'rm -f "$RESP_FILE"' EXIT

# ── helpers ───────────────────────────────────────────────────────────────────

green() { printf "\033[32m%s\033[0m\n" "$*"; }
red()   { printf "\033[31m%s\033[0m\n" "$*"; }
bold()  { printf "\033[1m%s\033[0m\n"  "$*"; }

# req — faz o request e salva JSON em $RESP_FILE (sem subshell nos contadores)
req() {
  local label="$1" subject="$2" payload="$3"

  local raw
  raw=$(nats req "$subject" "$payload" --server "$NATS_URL" --timeout 5s 2>&1)

  # nats CLI emite linhas de log antes do JSON — pega só a linha que começa com '{'
  local response
  response=$(echo "$raw" | grep -m1 '^{' || echo "{}")
  echo "$response" > "$RESP_FILE"

  local ok
  ok=$(python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('ok',''))" \
       < "$RESP_FILE" 2>/dev/null || echo "")

  if [ "$ok" = "True" ]; then
    green "  ✓ $label"
    PASS=$((PASS + 1))
  else
    red  "  ✗ $label"
    echo "    response: $response"
    FAIL=$((FAIL + 1))
  fi
}

# extract — lê campo do último response salvo em $RESP_FILE
extract() {
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d$1)" \
    < "$RESP_FILE" 2>/dev/null
}

# ── testes ────────────────────────────────────────────────────────────────────

bold "=== smoke_test :: prompt-ver-core ==="
echo "NATS: $NATS_URL"
echo ""

# 1. create_prompt
bold "1. create_prompt"
req "create_prompt" \
  "prompts.v1.commands.create_prompt" \
  '{"name":"smoke-test-prompt","content":"Initial version content"}'
PROMPT_ID=$(extract "['data']['id']")
echo "    prompt_id: $PROMPT_ID"
echo ""

# 2. add_version (v1)
bold "2. add_version (v1)"
req "add_version v1" \
  "prompts.v1.commands.add_version" \
  "{\"prompt_id\":\"$PROMPT_ID\",\"content\":\"Hello, world! Version 1\"}"
VERSION_ID_1=$(extract "['data']['id']")
echo "    version_id_1: $VERSION_ID_1"
echo ""

# 3. add_version (v2)
bold "3. add_version (v2)"
req "add_version v2" \
  "prompts.v1.commands.add_version" \
  "{\"prompt_id\":\"$PROMPT_ID\",\"content\":\"Hello, world! Version 2 — updated\"}"
VERSION_ID_2=$(extract "['data']['id']")
echo "    version_id_2: $VERSION_ID_2"
echo ""

# 4. update_content
bold "4. update_content"
req "update_content" \
  "prompts.v1.commands.update_content" \
  "{\"prompt_id\":\"$PROMPT_ID\",\"content\":\"Hello, world! Version 2 — edited\"}"
echo ""

# 5. activate_version (v1)
bold "5. activate_version (v1)"
req "activate_version v1" \
  "prompts.v1.commands.activate_version" \
  "{\"prompt_id\":\"$PROMPT_ID\",\"version_id\":\"$VERSION_ID_1\"}"
echo ""

# 6. activate_version (v2)
bold "6. activate_version (v2)"
req "activate_version v2" \
  "prompts.v1.commands.activate_version" \
  "{\"prompt_id\":\"$PROMPT_ID\",\"version_id\":\"$VERSION_ID_2\"}"
echo ""

# 7. get_prompt_by_id
bold "7. get_prompt_by_id"
req "get_prompt_by_id" \
  "prompts.v1.queries.get_prompt_by_id" \
  "{\"prompt_id\":\"$PROMPT_ID\"}"
echo ""

# 8. list_versions
bold "8. list_versions"
req "list_versions" \
  "prompts.v1.queries.list_versions" \
  "{\"prompt_id\":\"$PROMPT_ID\"}"
echo ""

# 9. list_active_prompts
bold "9. list_active_prompts"
req "list_active_prompts" \
  "prompts.v1.queries.list_active_prompts" \
  '{}'
echo ""

# 10. compare_versions
bold "10. compare_versions"
req "compare_versions" \
  "prompts.v1.queries.compare_versions" \
  "{\"prompt_id\":\"$PROMPT_ID\",\"version_id_before\":\"$VERSION_ID_1\",\"version_id_after\":\"$VERSION_ID_2\"}"
echo ""

# 11. soft_delete_prompt
bold "11. soft_delete_prompt"
req "soft_delete_prompt" \
  "prompts.v1.commands.soft_delete_prompt" \
  "{\"prompt_id\":\"$PROMPT_ID\"}"
echo ""

# 12. list_deleted_prompts
bold "12. list_deleted_prompts"
req "list_deleted_prompts" \
  "prompts.v1.queries.list_deleted_prompts" \
  '{}'
echo ""

# 13. recover_prompt
bold "13. recover_prompt"
req "recover_prompt" \
  "prompts.v1.commands.recover_prompt" \
  "{\"prompt_id\":\"$PROMPT_ID\"}"
echo ""

# ── resultado ─────────────────────────────────────────────────────────────────

bold "=== resultado ==="
green "  passou: $PASS"
[ "$FAIL" -gt 0 ] && red "  falhou: $FAIL" || echo "  falhou: $FAIL"
echo ""

[ "$FAIL" -eq 0 ]
