POSTGRES = "postgres://squjcergemukcq:5a67f4a028ff7ceadf351e26322380546ffd979bb70c8e8a1091c2707b49d14c@ec2-54-228-250" \
           "-82.eu-west-1.compute.amazonaws.com:5432/d7rs9bn804cvp2"

DB_FILE = "/db/comments.sqlite"  # если хотим оставить возможность переключиться обратно на sqlite
SQLITE = f'sqlite://{DB_FILE}?check_same_thread=False'

LOCAL_DB = POSTGRES
