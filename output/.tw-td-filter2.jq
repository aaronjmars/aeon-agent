.data.tweets[]
| select((.isReply // false) | not)
| [.author.userName, .createdAt, .likeCount, .retweetCount, .replyCount, .url, .text]
| @tsv
