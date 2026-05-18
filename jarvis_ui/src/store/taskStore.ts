type TaskState = {
    currentTask: string | null;
    taskData: any;
    taskHistory: { type: string; timestamp: number; data: any }[];
};

export const taskStore: TaskState = {
    currentTask: null,
    taskData: null,
    taskHistory: [],
};