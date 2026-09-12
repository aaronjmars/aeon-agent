.data.tweets[]
| select((.isReply // false) | not)
| (try (.createdAt | strptime("%a %b %d %H:%M:%S %z %Y") | strftime("%Y-%m-%d")) catch (.createdAt[0:10])) as $d
| select($d >= $since)
| [.author.userName, $d, .likeCount, .retweetCount, .replyCount, .url, .text] | @tsv
