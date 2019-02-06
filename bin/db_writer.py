import sqlite3

class db_operations:

    def __init__(self):
        self.conn = sqlite3.connect('../data/system_logs.db', uri=True)
        self.cursor = self.conn.cursor()

    def create_table(self, query):
        self.cursor.execute(query)
        self.conn.commit()
    
    def write_values(self, query, values):
        self.cursor.executemany(query, values)
        self.conn.commit()
    
    def close_database(self):
        self.conn.close()

class data_writer():

    def __init__(self, system, disk, battery, network, process):
        self.log_db = db_operations()
        self.system_data = system
        self.disk_data = disk
        self.battery_data = battery
        self.network_data = network
        self.process_data = process

    def write_all(self):
        self.write_system()
        self.write_disk()
        self.write_battery()
        self.write_network()
        self.write_process()
    
    def write_system(self):
        
        try:
            self.log_db.create_table('create table if not exists system_info (log_id text, log_date text,'
                'log_time text, os_family text, os_release text, os_platform text,'
                "os_version text, boot_date text, boot_time text, isp_name text,"
                'region text, accuracy text, asn text, isp_details text, timezone text, longitude text,'
                'short_country_name text, area_code text, public_ip text, city text, country text,'
                'continent_code text, country_code text, latitude text)')
        except:
            print('An error has occured while creating system information database.')

        try:
            self.log_db.write_values('insert into system_info values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [self.system_data])
            #print('System information data has been written to the database.')
        
        except:
            print('An error has occured while writing to system information database.')

    def write_disk(self):
        
        try:
            self.log_db.create_table('create table if not exists disks (log_id text, log_date text,'
                'log_time text, partition text, total_space text, used_space text, free_space text,'
                'used_percent text, file_system text, mount_point text)')
        except:
            print('An error has occured while creating disk information database.')
        
        try:
            self.log_db.write_values('insert into disks values (?,?,?,?,?,?,?,?,?,?)', self.disk_data)
            #print('Disk information data has been written to the database.')
        
        except:
            print('An error has occured while writing to disk information database.')

    def write_battery(self):
        
        try:
            self.log_db.create_table('create table if not exists battery (log_id text, log_date text, log_time text, battery_supported text,'
                'battery_available text, battery_percent text, battery_time_left text, charging_status text, plugged_in text)')
        except:
            print('An error has occured while creating battery information database.')
        
        try:
            self.log_db.write_values('insert into battery values (?,?,?,?,?,?,?,?,?)', [self.battery_data])
            #print('Battery information data has been written to the database.')
        
        except:
            print('An error has occured while writing to battery information database.')

    def write_network(self):
        
        try:
            self.log_db.create_table('create table if not exists network (log_id text, log_date text, log_time text, interface_name text,'
                'active text, speed text, duplex text, mtu text, incoming_bytes text, incoming_packets text, incoming_errors text,'
                'incoming_drops text, outgoing_bytes text, outgoing_packets text, outgoing_errors text, outgoing_drops text, ipv4_address text, ipv4_netmask text,'
                ' mac_address text, ipv6_address text, ipv6_netmask text)')
        except:
            print('An error has occured while creating network information database.')
        
        try:
            self.log_db.write_values('insert into network values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', self.network_data)
            #print('Network information data has been written to the database.')
        
        except:
            print('An error has occured while writing to network information database.')

    def write_process(self):
        
        try:
            self.log_db.create_table('create table if not exists process (log_id text, log_date text, log_time text, pid text,'
                'ppid text, pname text, cpu_usage text, memory_percent_usage text, memory_rss text,'
                'memory_vms text, exec_path text, user text, priority text)')
        except:
            print('An error has occured while creating process information database.')
        
        try:
            self.log_db.write_values('insert into process values (?,?,?,?,?,?,?,?,?,?,?,?,?)', self.process_data)
            #print('Process information data has been written to the database.')
        
        except:
            print('An error has occured while writing to process information database.')

def start_program(system, disk, battery, network, process):
    writer = data_writer(system, disk, battery, network, process)
    writer.write_all()
    writer.log_db.close_database()