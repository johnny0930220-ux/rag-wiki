"""記錄生成節點（N1～N6）做了什麼：python3 tools/log_node.py "N3 Ingest S1" "說明" """
import sys
from common import log

node, note = sys.argv[1], " ".join(sys.argv[2:])
log(node, True, [], {"說明": note})
print(f"已記錄：{node}｜{note}")
