# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

class WebhookStatements:
    init = "CREATE TABLE IF NOT EXISTS `webhooks` (" \
           "    id uuid PRIMARY KEY," \
           "    hook_type smallint," \
           "    guild varchar(32)," \
           "    channel varchar(32)," \
           "    role_mentions list<varchar(32)>," \
           "    user_mentions list<varchar(32)>" \
           ");"

    create = "INSERT INTO `webhooks` (id, hook_type, guild, channel, role_mentions, user_mentions) " \
             "VALUES (?, ?, ?, ?, ?, ?);"

    get = "SELECT * FROM `webhooks` " \
          "WHERE id = ?;"

    delete = "DELETE FROM `webhooks` " \
             "WHERE id = ?;"

    add_role_mention = "UPDATE `webhooks` " \
                       "SET role_mentions = role_mentions + [?] " \
                       "WHERE id = ?;"

    remove_role_mention = "UPDATE `webhooks` " \
                          "SET role_mentions = role_mentions - [?] " \
                          "WHERE id = ?;"

    add_user_mention = "UPDATE `webhooks` " \
                       "SET user_mentions = user_mentions + [?] " \
                       "WHERE id = ?;"

    remove_user_mention = "UPDATE `webhooks` " \
                          "SET user_mentions = user_mentions - [?] " \
                          "WHERE id = ?;"


class CQLStatements:
    keyspace_init = "CREATE KEYSPACE IF NOT EXISTS `{keyspace}` " \
                    "WITH replication = {" \
                    "   'class': 'NetworkTopologyStrategy'," \
                    "   'replication_factor': 3" \
                    "};"

    webhooks = WebhookStatements


stmt = CQLStatements
