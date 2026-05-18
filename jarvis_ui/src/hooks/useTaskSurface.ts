import { useState, useCallback } from 'react';
export function useTaskSurface() {
    const [activeTask, setActiveTask] = useState<string | null>(null);
    const [taskData, setTaskData] = useState<any>(null);
    const openTask = useCallback((type: string, data?: any) => { setActiveTask(type); setTaskData(data); }, []);
    const closeTask = useCallback(() => { setActiveTask(null); setTaskData(null); }, []);
    return { activeTask, taskData, openTask, closeTask };
}