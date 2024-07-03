# ChatAppWithFlet

## Contributors

| No  | Name                               | NRP   | Jobdesk |
|-----|------------------------------------|--------------|---------|
| 1   | Gabrielle Immanuel Osvaldo Kurniawan| 5025211135   | Implement protocol chatting & deployment |
| 2   | Sandyatama Fransisna Nugraha       | 5025211196   | Implement Flet Interface & deployment |
| 3   | Andrian                            | 5025211079   | Implement multirealm protocol & deployment |
| 4   | Duevano Fairuz Pandya              | 5025211052   | Implement multirealm protocol & deployment |
| 5   | Aryasatya Wiryawan                 | 5025221256   | Documentation and Testing & deployment |
| 6   | Muhammad febriansyah               | 5025211164   | Documentation and testing & deployment |

## Protokol

### Server Mesin1
Lokasi Port      : 8889
Lokasi Program   : .ChatAppWithFlet/Mesin1 (Chat App)/ChatServer.py

### Client Mesin1
Ip Destination    : 172.16.16.101
Port Destination  : 8889

### Server Mesin2
Lokasi Port      : 8890
Lokasi Program   : .ChatAppWithFlet/Mesin1 (Chat App)/ChatServer.py

### Client Mesin1
Ip Destination    : 172.16.16.102
Port Destination  : 8890

## Client Command Prompt

        1. Login: '''auth [username] [password]''' contoh "auth messi surabaya

        2. Register: '''register [username] [password] [nama (gunakan "_" untuk seperator) ] [negara]''' contoh '''register joni admin joni_perkasa Indonesia

        3. Buat group: '''addgroup [nama_group]''' contoh '''addgroup jarkom3'''

        4. Join group: '''joingroup [nama_group]''' contoh '''joingroup jarkom3'''

        5. Mengirim pesan private: '''send [username to] [message]''' contoh '''send messi hello world'''

        6. Mengirim file private: '''sendfile [username to] [filename]''' contoh '''sendfile messi file.txt'''

        7. Mengirim pesan ke group: '''sendgroup [nama_group] [message]''' contoh '''sendgroup jarkom3 hallo guys welcome'''

        8. Mengirim file ke group: '''sendgroupfile [usernames to] [filename]''' contoh sendgroupfile jarkom3 file.txt

        9. Melihat pesan: '''inbox'''

        10. Logout: '''logout'''

        11. Melihat user yang aktif: '''info'''

## Komunikasi dengan server lain



## Default Information


