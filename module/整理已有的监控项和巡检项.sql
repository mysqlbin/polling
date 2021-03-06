
目前已有的监控项和巡检项列表


1. 监控项
	
	1. 长事务：        每隔30秒检测一次，超过10秒的SQL语句则通过邮件报警
	2. 错误日志：      每隔5分钟检测一次，有异常则通过邮件报警
	3. 慢查询：        1个小时检测一次，有慢查询则通过邮件报警
	4. 主从复制监控：  1分钟检测一次，从库复制异常则通过邮件报警
	5. MySQL 状态监控：1分钟检测一次，连接不上MySQL则通过邮件报警
	6. DB3延迟从库的数据复制监控：每天的9点和18点检测一次 
	
2. 操作系统巡检
	每天的8点40分自动巡检，巡检结果通过邮件发送
	CPU： 核数、user使用率、system使用率
	内存：总内存、可用内存
	数据盘：总空间大小、剩余空间大小
	系统盘：总空间大小、剩余空间大小

3. 数据库层巡检
	
	把这些巡检的项目，
	
	一. 表检查
        对数据库实例下各个库下使用存储引擎类型的统计：非InnoDB存储引擎则
		超过多少5的表        
		数据量排名前20的表    
		单表超过行数1000W的表  
		碎片超过1G的表     
		自增ID占比: 观察已经使用的自增ID的大小超过50%的表             
        

	二. 索引检查
	    索引数目超过多少个的表
		无主键索引表

		#重复/冗余索引     #schema_redundant_indexes
		#字段过多索引
		#从未使用过的索引  #schema_unused_indexes
		#查看哪些索引采用部分索引（前缀索引）


	三. 参数检查(variables)

		#3.1. InnoDB 层
            
            tx_isolation
            innodb_rollback_on_timeout
            innodb_io_capacity 
            innodb_io_capacity_max
            innodb_autoinc_lock_mode
            innodb_flush_method
            innodb_file_per_table
            innodb_open_files
            innodb_data_home_dir
            innodb_lock_wait_timeout
            innodb_thread_concurrency
            innodb_fast_shutdown
            innodb_data_file_path
            innodb_write_io_threads
            innodb_read_io_threads
            innodb_purge_threads
            innodb_page_cleaners
            #double write:
                innodb_doublewrite
            #change buffer:
                innodb_change_buffer_max_size
                innodb_change_buffering
            #AHI:
                innodb_adaptive_hash_index



        #3.1.2. InnoDB Redo
            innodb_flush_log_at_trx_commit
            innodb_log_file_size
            innodb_log_files_in_group
            innodb_log_buffer_size
            innodb_flush_log_at_timeout: 定义每次日志刷新的时间, 默认是1，也就是每秒log刷盘
            Redo日志可写剩余空间：innodb_log_file_size*innodb_log_files_in_group - (Log flushed up to-Last checkpoint at)

        #3.1.3 InnoDB undo log


        #3.1.4 持久化统计信息
            innodb_stats_persistent
            innodb_stats_persistent_sample_pages
            innodb_stats_auto_recalc

		#3.2 Server 层
		3.2.1 binlog:

            sync_binlog
            binlog_format
            binlog_row_image
            binlog_cache_size
            max_binlog_cache_size
            max_binlog_size
            expire_logs_days

        3.2.2 数据库连接数:
		    max_connections
		    max_connect_errors
		    max_user_connections
            Max_used_connections  #状态值

        3.2.3 会话/线程级内存
            key_buffer_size
            query_cache_size
            read_buffer_size
            read_rnd_buffer_size
            sort_buffer_size
            join_buffer_size
            binlog_cache_size
            tmp_table_size
        3.2.4 其它参数
            sql_safe_updates
            max_allowed_packet
            table_open_cache
            max_execution_time
            sql_mode
            interactive_timeout
            wait_timeout
            open_files_limit
            lower_case_table_names
            slow_query_log
            long_query_time
            log_queries_not_using_indexes
            system_time_zone
            time_zone
            log_timestamps

        3.3 数据库连接数：
            max_connections
            max_connect_errors
            max_user_connections
            Max_used_connections  #状态值

	四. InnoDB buffer pool的使用情况:
	  4.1 参数:
        innodb_random_read_ahead              #随机预读
        innodb_read_ahead_threshold           #线性预读

	    innodb_buffer_pool_load_at_startup    #预热: 把热数据从磁盘load到buffer pool
        innodb_buffer_pool_dump_at_shutdown   #预热: 把热数据从buffer pool dump到磁盘
        innodb_flush_neighbors                #预写, SSD可以关闭，传统机械硬盘开启；

        innodb_buffer_pool_size               #缓冲池大小
        innodb_buffer_pool_instances          #缓冲池实例数
        innodb_lru_scan_depth                 #控制LRU列表中可用页的数量，默认值为1024
        innodb_max_dirty_pages_pct            #达到最大脏页占比，强制进行 checkpoint, 刷新一部分的脏页到磁盘
        innodb_old_blocks_pct                 #lru中旧区域数据的占比
        innodb_old_blocks_time                #控制lru中数据停留在old区域头部的时间

      4.2 状态值:
		innodb_buffer_pool_pages_dirty            #脏页数据的大小;     单位是Page
		innodb_buffer_pool_pages_total            #缓冲池总共的页面数; 单位是Page
		innodb_buffer_pool_read_requests          #从缓冲池读取页的次数
		#预读的状态监控
		innodb_buffer_pool_read_ahead             #预读的页数
        Innodb_buffer_pool_read_ahead_evicted     #无效的预读页数，即通过预读把数据页读取内存，但是没有被使用就被淘汰的页数

		innodb_buffer_pool_reads                  #从磁盘读取页的次数
		Innodb_buffer_pool_pages_data             #分配出去，正在被使用page的数量，包括脏页；单位是Page
        Innodb_buffer_pool_pages_free             #空闲的page数量; 单位是Page
	    Innodb_buffer_pool_wait_free              #状态参数；buffer pool free list(空闲列表)暂无空闲可用的页，需要等于申请，大于0 说明 InnoDB buffer pool 内存紧张。

	  4.3 计算脏页占比:
	    innodb_buffer_pool_pages_dirty/innodb_buffer_pool_pages_total
	  4.4 计算InnoDB buffer pool 命中率:
	     innodb_buffer_pool_read_requests/(innodb_buffer_pool_read_requests + innodb_buffer_pool_read_ahead + innodb_buffer_pool_reads)
	  4.5 判断 InnoDB buffer pool是否使用紧张(不够用)：
	     查看 Innodb_buffer_pool_wait_free 的值是否大于0， 大于0说明紧张


	五. 状态值:
	  https://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html
	  5.1 当前并发连接数:
		Threads_connected  并发连接数（表示当前所有已经连接的线程数）
		Threads_created    表示当前所有已经创建的线程数
		Threads_running    并发活跃线程数（表示当前正在运行的线程数）
		
	  5.2 行锁等待:
		
		Innodb_row_lock_current_waits  表示当前发生行锁等待的次数
		Innodb_row_lock_time        表示当前发生行锁等待的总时间（以毫秒为单位）
		Innodb_row_lock_time_avg    表示当前发生行锁等待的平均时间（以毫秒为单位）
		Innodb_row_lock_time_max    表示当前发生行锁等待的最大时间（以毫秒为单位）
		Innodb_row_lock_waits       表示发生行锁等待的总次数
	    如果 Innodb_row_lock_time_avg 跟 Innodb_row_lock_time_max 的差值很大 ，需要看慢SQL;

	  5.3 打开表的次数:
	    Open_files
	    opend_tables
        Opened_tables

      5.4 创建的内存临时表和磁盘临时表的次数:
        Created_tmp_tables
        Created_tmp_disk_tables

      5.5 double write的使用情况:
        Innodb_dblwr_pages_written
        Innodb_dblwr_writes

      5.6 因 log buffer不足导致等待写redo的次数:
        Innodb_log_waits
        https://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html#statvar_Innodb_log_waits
        The number of times that the log buffer was too small and a wait was required for it to be flushed before continuing.

    六、长事务、临时表、行锁等待列表:

	 6.1 长时间未提交的事务
	    select b.host, b.user, b.db, b.time, b.COMMAND, a.trx_id, a. trx_state from information_schema.innodb_trx a left join information_schema.PROCESSLIST b on a.trx_mysql_thread_id = b.id;
	 6.2 哪些SQL语句使用了磁盘临时表?
        select db, query, tmp_tables, tmp_disk_tables, tmp_tables+tmp_disk_tables as tmp_all from sys.statement_analysis where tmp_tables>0 or tmp_disk_tables >0 order by tmp_all desc limit 20;

	 6.3 行锁等待
	    SELECT * FROM sys.innodb_lock_waits

	 #表锁
	 #死锁
	 #MDL锁

    七、实例下的所有用户和对应的权限

    账号所需权限：
        grant process,select on *.* to 'polling_user'@'%' identified by '123456abc';

    八、复制相关参数
    server id
    log_slave_updates
    slave-parallel-type                     #MySQL 5.7     新增
    slave_parallel_workers

    binlog_group_commit_sync_delay
    binlog_group_commit_sync_no_delay_count
    binlog-transaction-dependency-tracking  #MySQL 5.7.22 新增, 基于 writeset的并行复制

    master_info_repository
    relay_log_info_repository
    relay_log_recovery

    #GTID:
        gtid_mode
        enforce_gtid_consistency

    #半同步复制


    parallel

	数据库统计信息：
	    数据库的总量  #select concat(round(sum(data_length + index_length) / 1024 / 1024, 2),'M') as total_mb from information_schema.tables where TABLE_SCHEMA='niuniu_db'
        共有多少个表  #SELECT COUNT( * ) FROM information_schema.tables WHERE TABLE_SCHEMA = 'niuniu_db'
        共有多少个存储过程
        共有多少个事件
	






