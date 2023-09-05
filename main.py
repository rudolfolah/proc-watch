import collections
import enum
import os
import os.path
import re
import subprocess
import sys

import prometheus_client


PS_KEYS = 'started,user,pid,ppid,time,cpu,mem,rss,vsz,state,comm,command'.split(',')
PS_KEYS_INTS = 'pid,ppid,mem,rss'.split(',')
PS_KEYS_FLOATS = 'cpu'.split(',')
PROM_EXPORT_PATH_DEFAULT = '/tmp/proc_watch.prom'


def get_ps_command_args() -> str:
    # Based on https://github.com/y-ken/fluent-plugin-watch-process/blob/master/lib/fluent/plugin/in_watch_process.rb#L106-L114
    match sys.platform:
        case 'darwin':
            return '-ewwo lstart,user,pid,ppid,time,%%cpu,%mem,rss,vsz,state,comm,command'
        case 'linux':
            return '-ewwo lstart,user:20,pid,ppid,time,%cpu,%mem,rss,sz,s,comm,cmd'
        case _:
            raise NotImplementedError


def run_ps_command() -> subprocess.CompletedProcess[str]:
    args = get_ps_command_args()
    env = { 'LANG': 'en_US.UTF-8' }
    return subprocess.run(args=args, executable='ps', shell=True, capture_output=True, text=True, env=env)


def set_ps_values(data: dict, keys: list[str], parse_func: callable):
    for key in keys:
        data[key] = parse_func(data[key])


def parse_ps_line(line: str) -> dict:
    # Based on https://github.com/y-ken/fluent-plugin-watch-process/blob/master/lib/fluent/plugin/in_watch_process.rb#L87-L98
    timestamp_match = re.match(r'(^\w+\s+\w+\s+\d+\s+\d\d:\d\d:\d\d \d+)', line)
    timestamp = timestamp_match.group(0)
    values = re.split(r'[ ]+', line[len(timestamp):].strip())
    data = dict(zip(PS_KEYS, [timestamp] + values))
    set_ps_values(data, PS_KEYS_INTS, int)
    set_ps_values(data, PS_KEYS_FLOATS, float)
    return data


def set_stats_info_for_process(stats: prometheus_client.Info, data: dict):
    stats.info({
        'process': str(data['comm']),
        'cpu': str(data['cpu']),
        'mem': str(data['mem']),
    })


def main():
    registry = prometheus_client.CollectorRegistry()
    stats_num_processes = prometheus_client.Gauge('num_processes', 'Number of processes running', registry=registry)
    stats_top_cpu = prometheus_client.Gauge('top_cpu', 'Top CPU usage, one process', registry=registry)
    stats_top_memory = prometheus_client.Gauge('top_mem', 'Top Memory usage, one process', registry=registry)
    stats_top_cpu_process = prometheus_client.Info('top_cpu_process', 'The process with top CPU usage', registry=registry)
    stats_top_memory_process = prometheus_client.Info('top_mem_process', 'The process with top Memory usage', registry=registry)

    completed = run_ps_command()
    processes = [parse_ps_line(line) for line in completed.stdout.split('\n')[1:] if len(line) > 0]
    stats_num_processes.set(len(processes))
    top_cpu = max(processes, key=lambda process: process['cpu'])
    stats_top_cpu.set(top_cpu['cpu'])
    set_stats_info_for_process(stats_top_cpu_process, top_cpu)
    top_memory = max(processes, key=lambda process: process['mem'])
    stats_top_memory.set(top_memory['mem'])
    set_stats_info_for_process(stats_top_memory_process, top_memory)

    prometheus_client.write_to_textfile(os.environ.get('PROM_EXPORT_PATH', PROM_EXPORT_PATH_DEFAULT), registry)


if __name__ == "__main__":
    main()
