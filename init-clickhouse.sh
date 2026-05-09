#!/bin/bash

NODES=(clickhouse-node1 clickhouse-node2 clickhouse-node3 clickhouse-node4)

# Wait for nodes
for host in "${NODES[@]}"; do
  until clickhouse-client --host $host --query "SELECT 1" 2>/dev/null; do
    sleep 2
  done
done


for host in "${NODES[@]}"; do
  clickhouse-client --host $host --query "CREATE DATABASE IF NOT EXISTS kafka_events"

  clickhouse-client --host $host --query "
    CREATE TABLE IF NOT EXISTS kafka_events.events_local (
      event_id UUID DEFAULT generateUUIDv4(),
      user_id UInt64,
      type String,
      value String,
      ts DateTime64(6)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(ts)
    ORDER BY (ts, event_id)
    SETTINGS index_granularity = 8192;
  "
done

clickhouse-client --host clickhouse-node1 --query "
  CREATE TABLE IF NOT EXISTS kafka_events.events (
    event_id UUID DEFAULT generateUUIDv4(),
    user_id UInt64,
    type String,
    value String,
    ts DateTime64(6)
  ) ENGINE = Distributed('company_cluster', 'kafka_events', 'events_local', rand());
"

echo 'ClickHouse cluster setup complete!'