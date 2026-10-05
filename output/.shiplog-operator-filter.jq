.data.tweets[]
| (try (.createdAt | strptime("%a %b %d %H:%M:%S %z %Y") | strftime("%Y-%m-%d")) catch (.createdAt[0:10])) as $d
| select($d >= "2026-09-28")
| [.id, $d, .isReply, .likeCount, .retweetCount, .replyCount, .url, (.text | gsub("\n";" "))] | @tsv
