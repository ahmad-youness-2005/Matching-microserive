import os
import json
import time
import subprocess
import socket
import psutil
import requests
from sqlalchemy import create_engine, text
import psycopg2
from typing import List, Tuple
from TestSmokingStatus import TestSmokingStatus
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class TestMatchingService:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_prefix = "/api/v1"
        self.health_url = f"{self.base_url}/health"
        
        self.container_name = "matching-microservice"
        self.image_name = "matching-microservice:latest"
        self.db_connection = None
        self.max_retries = 60
        self.retry_interval = 2
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not found")
        
        parsed_url = urlparse(database_url)
        self.db_name = parsed_url.path.lstrip('/')
        self.db_user = parsed_url.username
        self.db_password = parsed_url.password
        self.db_host = parsed_url.hostname
        self.db_port = parsed_url.port or "5432"
        
        print(f"Database configuration: host={self.db_host}, port={self.db_port}, database={self.db_name}")
        
    def setup(self):
        print("--------------------------------Test started--------------------------------")
        self.cleanup_docker_resources()
        self.drop_database_tables()
        
        if not self.build_docker_image():
            print("⚠️ Warning: Failed to build Docker image")
            return False
            
        if not self.start_docker_container():
            print("⚠️ Warning: Failed to start Docker container")
            return False
            
        if not self.wait_for_service():
            print("⚠️ Warning: Service health check failed, but continuing anyway")
            
        return True
    
    def teardown(self):
        print("--------------------------------Test cleanup--------------------------------")
        self.cleanup_docker_resources()
    
    def check_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
            
    def kill_process_on_port(self, port):
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        proc.kill()
                        time.sleep(1)
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
        
    def cleanup_docker_resources(self):
        print("\nCleaning up Docker resources...")
        
        subprocess.run(["docker", "stop", self.container_name], capture_output=True)
        subprocess.run(["docker", "rm", self.container_name], capture_output=True)
        
        subprocess.run(["docker", "rmi", self.image_name], capture_output=True)
        
        print("Cleanup completed")
        
    def get_database_connection(self):
        db_user = "ahmadyounes"
        db_password = "newpassword"
        db_host = "192.168.1.28"
        db_port = "5432"
        db_name = "matching"
        
        engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        return engine

    def verify_tables(self):
        print("\nVerifying database tables...")
        try:
            engine = self.get_database_connection()
            
            table_info_query = """
                SELECT 
                    t.table_name,
                    array_agg(c.column_name || ' ' || c.data_type) as columns
                FROM information_schema.tables t
                JOIN information_schema.columns c 
                    ON t.table_name = c.table_name
                WHERE t.table_schema = 'public'
                    AND t.table_type = 'BASE TABLE'
                GROUP BY t.table_name
                ORDER BY t.table_name;
            """
            
            with engine.connect() as connection:
                print("\nCurrent database tables and their structure:")
                result = connection.execute(text(table_info_query))
                tables_info = result.fetchall()
                
                if tables_info:
                    for table_name, columns in tables_info:
                        print(f"\nTable: {table_name}")
                        print("Columns:")
                        for column in columns:
                            print(f"  - {column}")
                else:
                    print("No tables found in the database")
                
                print("\nTable row counts:")
                for table_name, _ in tables_info:
                    count_result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = count_result.scalar()
                    print(f"- {table_name}: {count} rows")
                
            return True
            
        except Exception as e:
            print(f"\nError verifying tables: {str(e)}")
            print("Stack trace:")
            import traceback
            traceback.print_exc()
            return False
            
    def drop_database_tables(self):
        print("\nDropping database tables...")
        try:
            engine = self.get_database_connection()
            
            table_query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE';
            """
            
            
            print("\nVerifying existing tables before deletion:")
            self.verify_tables()
            
            with engine.connect() as connection:
                print("\nDropping tables...")
                result = connection.execute(text(table_query))
                tables = [row[0] for row in result]
                
                if tables:
                    for table in tables:
                        print(f"Dropping table: {table}")
                        connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    connection.commit()
                    print("All tables dropped successfully")
                else:
                    print("No tables to drop")
                
                print("\nVerifying database state after deletion:")
                result = connection.execute(text(table_query))
                remaining_tables = [row[0] for row in result]
                if remaining_tables:
                    print("Warning: Some tables still exist:")
                    for table in remaining_tables:
                        print(f"- {table}")
                else:
                    print("All tables successfully dropped")
            
            return True
            
        except Exception as e:
            print(f"\nError dropping database tables: {str(e)}")
            print("Stack trace:")
            import traceback
            traceback.print_exc()
            return False

    def wait_for_tables_creation(self, max_retries=30, retry_interval=1):
        print("\nWaiting for database tables to be created...")
        retries = 0
        while retries < max_retries:
            try:
                engine = self.get_database_connection()
                with engine.connect() as connection:
                    result = connection.execute(text("""
                        SELECT COUNT(*) 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                        AND table_type = 'BASE TABLE';
                    """))
                    table_count = result.scalar()
                    
                    if table_count > 0:
                        print(f"Tables created successfully! Found {table_count} tables.")
                        self.verify_tables()
                        return True
                    
                    print(f"No tables found yet. Retry {retries + 1}/{max_retries}")
                    
            except Exception as e:
                print(f"Error checking tables: {str(e)}")
            
            retries += 1
            time.sleep(retry_interval)
        
        raise TimeoutError("Tables were not created in time")

    def build_docker_image(self):
        print("\nBuilding Docker image...")
        try:
            subprocess.run(["docker", "rmi", "-f", self.image_name], capture_output=True, text=True)
            print("Removed existing Docker image")
            
            process = subprocess.run(
                ["docker", "build", "-t", self.image_name, "-f", "../Dockerfile", ".."],
                capture_output=True,
                text=True
            )
            
            print("STDOUT:", process.stdout)
            print("STDERR:", process.stderr)
            
            if process.returncode != 0:
                print(f"❌ Error building Docker image: {process.stderr}")
                return False
            
            print("✅ Docker image built successfully")
            return True
        except Exception as e:
            print(f"❌ Error building Docker image: {str(e)}")
            return False
            
    def start_docker_container(self):
        print("\nStarting Docker container...")
        try:
            subprocess.run(["docker", "rm", "-f", self.container_name], capture_output=True, text=True)
            print("Removed existing container")
            
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise Exception("DATABASE_URL environment variable not found")
                
            result = subprocess.run([
                "docker", "run",
                "-d",
                "--name", self.container_name,
                "-p", "8000:8090",
                "-e", f"DATABASE_URL={database_url}",
                self.image_name
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Error starting container: {result.stderr}")
                return False
            
            print("✅ Container started successfully")
            
            print("Waiting 6 seconds for container initialization...")
            time.sleep(6)
            
            status = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Status}}", self.container_name],
                capture_output=True,
                text=True
            )
            print(f"Container status: {status.stdout.strip()}")
            
            self.monitor_container_logs()
            
            if status.stdout.strip() != "running":
                print(f"❌ Container is not running: {status.stdout.strip()}")
                return False
                
            return True
        except Exception as e:
            print(f"❌ Error starting container: {str(e)}")
            return False
            
    def monitor_container_logs(self):
        try:
            print("\n=== Container Logs ===")
            subprocess.run(
                ["docker", "logs", self.container_name],
                capture_output=False,
                text=True
            )
        except Exception as e:
            print(f"Error getting container logs: {str(e)}")
            
    def wait_for_service(self, max_retries=30, retry_interval=3):
        print(f"Waiting for the service to be ready (max {max_retries} attempts)...")
        
        health_url = self.health_url
        
        for attempt in range(1, max_retries + 1):
            try:
                print(f"Attempt {attempt}/{max_retries}: Checking if service is ready...")
                response = requests.get(health_url, timeout=10)
                
                if response.status_code == 200:
                    print(f"Service is ready! Response: {response.text[:100]}")
                    return True
                else:
                    print(f"Service returned unexpected status: {response.status_code}, Response: {response.text[:100]}")
            except requests.exceptions.RequestException as e:
                print(f"Service not ready yet: {str(e)}")
            
            logs = subprocess.run(
                ["docker", "logs", "--tail", "20", self.container_name],
                capture_output=True,
                text=True
            )
            print(f"Recent container logs:\n{logs.stdout}")
            
            time.sleep(retry_interval)
        
        print(f"Service failed to become ready after {max_retries} attempts")
        return False

    def connect_to_database(self) -> None:
        print("\nAttempting to connect to database...")
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                self.db_connection = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    host=self.db_host,
                    port=self.db_port
                )
                print("Successfully connected to database")
                return
            except psycopg2.OperationalError as e:
                retry_count += 1
                print(f"Database connection attempt {retry_count}/{self.max_retries} failed: {str(e)}")
                time.sleep(self.retry_interval)
        
        raise Exception("Failed to connect to database after maximum retries")

    def get_all_tables(self) -> List[str]:
        if not self.db_connection:
            raise Exception("No database connection available")
            
        with self.db_connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            return [row[0] for row in cursor.fetchall()]

    def drop_all_tables(self) -> None:
        print("\nDropping existing tables...")
        if not self.db_connection:
            raise Exception("No database connection available")
            
        tables = self.get_all_tables()
        
        if not tables:
            print("No tables to drop")
            return
            
        print("\nTable row counts:")
        for table in tables:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"- {table}: {count} rows")
            except Exception as e:
                print(f"Error getting row count for {table}: {str(e)}")
        
        print("\nDropping tables...")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    DO $$ DECLARE
                        r RECORD;
                    BEGIN
                        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                        END LOOP;
                    END $$;
                """)
                self.db_connection.commit()
        except Exception as e:
            print(f"Error dropping tables: {str(e)}")
        
        print("All tables dropped successfully")

    def verify_database_state(self) -> None:
        tables = self.get_all_tables()
        if tables:
            raise Exception(f"Database not clean. Found tables: {', '.join(tables)}")
        print("\nVerifying database state after deletion:")
        print("All tables successfully dropped")

    def test_service_health(self) -> None:
        print("Testing service health...")
        try:
            health_url = self.health_url
            print(f"Checking health endpoint: {health_url}")
            response = requests.get(health_url, timeout=5)
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            print(f"Service health check passed. Response: {response.text[:100]}")
        except Exception as e:
            print(f"Service health check failed: {str(e)}")
            raise

    def verify_table_creation(self) -> None:
        print("\nWaiting for database tables to be created...")
        
        retry_count = 0
        while retry_count < self.max_retries:
            tables = self.get_all_tables()
            if len(tables) > 0:
                print(f"\nTables created successfully. Found {len(tables)} tables:")
                for table in tables:
                    print(f"- {table}")
                return
            
            retry_count += 1
            print(f"No tables found yet. Retry {retry_count}/{self.max_retries}")
            time.sleep(self.retry_interval)
        
        raise Exception("Tables were not created in time")

    def cleanup(self) -> None:
        print("\n--------------------------------Test cleanup--------------------------------")
        print("\nCleaning up Docker resources...")
        
        if self.db_connection:
            self.db_connection.close()
            print("Database connection closed")
        
        try:
            subprocess.run(["docker", "stop", self.container_name], capture_output=True, text=True)
            subprocess.run(["docker", "rm", self.container_name], capture_output=True, text=True)
            print("Cleanup completed")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def run_tests(self):
        try:
            print("\n=== Starting Tests ===")
           
            
            self.connect_to_database()
            
            self.drop_all_tables()
            self.verify_database_state()

            self.setup()

            self.test_service_health()
            self.verify_table_creation()
            
            self.runAllTests()

            print("\n✅ All tests passed successfully!")
            return True
            
        except AssertionError as e:
            print(f"\n❌ Test failed: {str(e)}")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            return False
        finally:
            self.teardown()

    def runAllTests(self):
        smoking = TestSmokingStatus()
        smoking.run_smoking_status_operations()

if __name__ == "__main__":
    test_suite = TestMatchingService()
    success = test_suite.run_tests()
    exit(0 if success else 1) 