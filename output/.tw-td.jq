.data.tweets[]
| select((.isReply // false) | not)
| (try (.createdAt | strptime("%a %b %d %H:%M:%S %z %Y") | strftime("%Y-%m-%d")) catch (.createdAt[0:10])) as $d
| select($d >= "2026-09-27")
| [.author.userName, $d, (.likeCount|tostring), (.retweetCount|tostring), (.replyCount|tostring), .url, (.isRetweet|tostring), .text] | @tsv
