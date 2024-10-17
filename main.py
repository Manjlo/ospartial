
class Process:
    def __init__(self, name,bt, at, queue, priority):
        self.name = name
        self.at = at
        self.bt = bt
        self.queue = queue
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0
        self.completion_time = 0
        self.remaining_time = bt
        self.first_response = True

    def __str__(self):
        return f"Process: {self.name}, Arrival Time: {self.at}, Burst Time: {self.bt}, Priority: {self.priority}"


class OrderAlgorithm:
    def __init__(self):
        self.name = "Algorithm"
        self.processes = []
        self.process1 = []
        self.process2 = []
        self.process3 = []
        self.current_time = 0

    def add_process(self, name, at, bt, priority):
        process = Process(name, at, bt, priority)
        self.processes.append(process)


    def get_process(self, queueNumber):
        if queueNumber == 1:
            return self.process1
        elif queueNumber == 2:
            return self.process2
        elif queueNumber == 3:
            return self.process3
        else:
            return self.processes


    def FCFS(self, queueNumber):
        processes = self.get_process(queueNumber)
        
        for process in processes:
            process.waiting_time = self.current_time - process.at
            process.completion_time = self.current_time + process.bt
            process.turnaround_time = process.completion_time - process.at
            process.response_time = process.waiting_time
            self.current_time += process.bt  # Usa self.current_time

    def SJF(self, queueNumber):
        processes = self.get_process(queueNumber)
        processes.sort(key=lambda x: x.at)

        completed_processes = []
        remaining_processes = processes[:]  # Copia de la lista de procesos para manipulación

        while remaining_processes:
            available_processes = [p for p in remaining_processes if p.at <= self.current_time]
        
            if available_processes:
                available_processes.sort(key=lambda x: x.bt)
                current_process = available_processes[0]

                current_process.waiting_time = self.current_time - current_process.at
                current_process.completion_time = self.current_time + current_process.bt
                current_process.turnaround_time = current_process.completion_time - current_process.at
                current_process.response_time = current_process.waiting_time
            
                self.current_time += current_process.bt  # Usa self.current_time

                completed_processes.append(current_process)
                remaining_processes.remove(current_process)
            else:
                self.current_time = min(remaining_processes, key=lambda x: x.at).at


    def STCF(self, queueNumber):
        process = self.get_process(queueNumber)
        process.sort(key=lambda x: x.at)

        remaining_processes = list(process)  # copia de procesos
        completed_processes = []  # lista de procesos completados

        while remaining_processes:
            available_processes = [p for p in remaining_processes if p.at <= self.current_time]

            if available_processes:
                current_process = min(available_processes, key=lambda x: x.remaining_time)

                if current_process.first_response:
                    current_process.response_time = self.current_time - current_process.at
                    current_process.first_response = False
                
                current_process.remaining_time -= 1
                self.current_time += 1  # Usa self.current_time

                if current_process.remaining_time == 0:
                    current_process.completion_time = self.current_time
                    current_process.turnaround_time = current_process.completion_time - current_process.at
                    current_process.waiting_time = current_process.turnaround_time - current_process.bt 
                    completed_processes.append(current_process)
                    remaining_processes.remove(current_process)
            else:
                if remaining_processes:
                    self.current_time = min(p.at for p in remaining_processes)


    def RR(self, quantum, queueNumber):
        processes = self.get_process(queueNumber)
        remaining_processes = list(processes)
        completed_processes = []
        
        while remaining_processes:
            current_process = remaining_processes[0]
            if current_process.at > self.current_time:
                self.current_time = current_process.at  # Mover el tiempo al próximo tiempo de llegada
        
            if current_process.first_response:
                current_process.response_time = self.current_time - current_process.at
                current_process.first_response = False

            current_process.remaining_time -= quantum
            if current_process.remaining_time < 0:
                self.current_time += quantum + current_process.remaining_time
                current_process.remaining_time = 0
            else:
                self.current_time += quantum

            if current_process.remaining_time == 0:
                current_process.completion_time = self.current_time
                current_process.turnaround_time = current_process.completion_time - current_process.at
                current_process.waiting_time = current_process.turnaround_time - current_process.bt
                completed_processes.append(current_process)
                remaining_processes.remove(current_process)

            remaining_processes.remove(current_process)
            remaining_processes.append(current_process)

                    
    def load_processes(self, url):
        with open(file_url, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue  # skip comments
                parts = line.strip().split(';')
                if len(parts) == 5:  # if line has 5 parts
                    name = parts[0].strip()
                    bt = int(parts[1].strip())
                    at = int(parts[2].strip())
                    queue = int(parts[3].strip())
                    priority = int(parts[4].strip())
                    self.add_process(label, bt, at, queue, priority)
                else:
                    print(f"No hay la suficiente informacion")
                    break
            file.close()


    def write_to_file(filename, processes):
        with open(filename, 'w') as file:
        # Escribir encabezado
            file.write("# archivo: {}\n".format(filename))
            file.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")

            total_wt = 0
            total_ct = 0
            total_rt = 0
            total_tat = 0

        # Escribir información de cada proceso
            for process in processes:
            # Suponiendo que cada proceso tiene los siguientes atributos:
            # name, bt, at, queue, priority, waiting_time, completion_time, response_time, turnaround_time
            line = "{}; {}; {}; {}; {}; {}; {}; {}; {}\n".format(
                process.name,
                process.bt,
                process.at,
                process.queue,
                process.priority,
                process.waiting_time,
                process.completion_time,
                process.response_time,
                process.turnaround_time
            )
            file.write(line)
            
            # Acumular totales para WT, CT, RT y TAT
            total_wt += process.waiting_time
            total_ct += process.completion_time
            total_rt += process.response_time
            total_tat += process.turnaround_time

        # Escribir promedios
        num_processes = len(processes)
        if num_processes > 0:
            file.write("WT={:.1f}; CT={:.1f}; RT={:.1f}; TAT={:.1f};\n".format(
                total_wt / num_processes,
                total_ct / num_processes,
                total_rt / num_processes,
                total_tat / num_processes
            ))

# Ejemplo de uso
# write_to_file('mlq001.txt', self.processes)

    def execute_scheduling_algorithms(self, algorithms, file_url):
        self.processes = load_processes_from_file(file_url)  # Cargar procesos desde el archivo
        for algorithm in algorithms.split(','):
            algorithm = algorithm.strip()  # Limpiar espacios en blanco
            if algorithm == 'fcfs':
                print("Ejecutando algoritmo FCFS...")
                self.FCFS()  # Llamar al método FCFS
            elif algorithm.startswith('rr'):
                quantum = int(algorithm[2:])  # Obtener el quantum
                print(f"Ejecutando Round Robin con quantum {quantum}...")
                self.RR(quantum)  # Llamar al método RR
            elif algorithm == 'sjf':
                print("Ejecutando algoritmo SJF...")
                self.SJF()  # Llamar al método SJF
            elif algorithm == 'stcf':
                print("Ejecutando algoritmo STCF...")
                self.STCF()  # Llamar al método STCF
            else:
                print(f"Algoritmo desconocido: {algorithm}")


