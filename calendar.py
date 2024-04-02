from datetime import datetime, timedelta
import time
import threading


class TaskManager:
    _instance = None

    def _new_(cls, *args, **kwargs):
        if not cls._instance:
            cls.instance = super(TaskManager, cls).new_(cls, *args, **kwargs)
            cls._instance.tasks = []
            cls._instance.completed_tasks = []
        return cls._instance

    def add_task(self, title, description, due_date=None):
        task = {"title": title, "description": description, "due_date": due_date}
        self.tasks.append(task)

    def mark_task_as_completed(self, task_index):
        task = self.tasks.pop(task_index)
        self.completed_tasks.append(task)

    def get_pending_tasks(self):
        return self.tasks

    def get_completed_tasks(self):
        return self.completed_tasks

    def search_task(self, title):
        for index, task in enumerate(self.tasks):
            if task["title"] == title:
                return index, task
        return None, None


class TaskNotifier(threading.Thread):
    def _init_(self, task_manager):
        super(TaskNotifier, self)._init_()
        self.task_manager = task_manager
        self.daemon = True

    def final(self):
        while True:
            tasks = self.task_manager.get_pending_tasks()
            for task in tasks:
                if task["due_date"] is not None and task["due_date"] <= datetime.now() + timedelta(days=1):
                    print(f"¡Recordatorio! La tarea '{task['title']}' vence pronto.")
            time.sleep(60)  # Verificar cada minuto


def get_date_input(prompt):
    while True:
        try:
            date_str = input(prompt)
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Formato de fecha incorrecto. Por favor, ingrese la fecha en formato YYYY-MM-DD.")


if _name_ == "_main_":
    task_manager = TaskManager()

    
    notifier = TaskNotifier(task_manager)
    notifier.start()

    while True:
        print("\n1. Porfavor agrega una tarea")
        print("2. Marcar tarea como completada")
        print("3. Buscar tarea")
        print("4. Mostrar tareas pendientes")
        print("5. Mostrar tareas completadas")
        print("6. Exit")

        choice = input("\nSeleccione una opción: ")

        if choice == "1":
            title = input("Ingrese el nombre de la tarea: ")
            description = input("IAñade la descripcion de la tarea: ")
            due_date_str = input("Ingrese la fecha de vencimiento (YYYY-MM-DD), o presione Enter para omitir: ")
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            else:
                due_date = None
            task_manager.add_task(title, description, due_date)
            print("Se añado correctamente la tarea.")

        elif choice == "2":
            title = input("Ingrese el nombre de la tarea que desea marcar como completada: ")
            index, task = task_manager.search_task(title)
            if task:
                task_manager.mark_task_as_completed(index)
                print(f"Tarea '{title}' marcada como completada.")
            else:
                print("Tarea no encontrada.")

        elif choice == "3":
            title = input("Ingrese el nombre de la tarea que desea buscar: ")
            index, task = task_manager.search_task(title)
            if task:
                print(f"Tarea encontrada:")
                print(f"Nombre: {task['title']}")
                print(f"Descripción: {task['description']}")
                if task["due_date"]:
                    print(f"Fecha de vencimiento: {task['due_date']}")
            else:
                print("Tarea no encontrada.")

        elif choice == "4":
            pending_tasks = task_manager.get_pending_tasks()
            if pending_tasks:
                print("\nTareas pendientes:")
                for task in pending_tasks:
                    print(f"{task['title']} - {task['description']} - Vence el {task['due_date']}")
            else:
                print("No hay tareas pendientes.")

        elif choice == "5":
            completed_tasks = task_manager.get_completed_tasks()
            if completed_tasks:
                print("\nTareas completadas:")
                for task in completed_tasks:
                    print(f"{task['title']} - {task['description']}")
            else:
                print("Tareas incompletas.")

        elif choice == "6":
            break

        else:
            print("Porfavor seleccione una opcion valida")

