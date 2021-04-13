# Shutting down a node

It’s possible to shutdown server on fly, but that would lead to failure of some queries.  
  
More safer way:

* Remove server \(which is going to be disabled\) from remote\_server section of config.xml on all servers.
* Remove server from load balancer, so new queries wouldn’t hit it.
* Wait until all already running queries would finish execution on it.  
  It’s possible to check it via query:

  ```text
  SHOW PROCESSLIST;
  ```

* Run sync replica query in related shard replicas via query:

  ```text
  SYSTEM SYNC REPLICA db.table;
  ```

* Shutdown server.

  
  
`SYSTEM SHUTDOWN` query doesn’t wait until query completion and tries to kill all queries immediately after receiving signal, even if there is setting `shutdown_wait_unfinished`.  
  
[https://github.com/ClickHouse/ClickHouse/blob/master/programs/server/Server.cpp\#L1353](https://github.com/ClickHouse/ClickHouse/blob/master/programs/server/Server.cpp#L1353)  
  
Можно просто потушить, но те запросы что сейчас выполняются на этой реплике умрут.

Можно сделать так:

Убрать данный сервер из remote\_server конфигов других серверов.

Убрать его из лоад балансера.

Подождать, пока на нем перестанут выполнятся запросы.

Выполнить SYSTEM SYNC REPLICA db.table на его соседе по репликации.

Потушить сервер.

© 2021 Altinity Inc. All rights reserved.
