type SystemState = {
    cpuUsage: number;
    ramUsage: number;
    gpuUsage: number;
    diskUsage: number;
    networkUp: number;
    networkDown: number;
    uptime: number;
};

export const systemStore: SystemState = {
    cpuUsage: 0,
    ramUsage: 0,
    gpuUsage: 0,
    diskUsage: 0,
    networkUp: 0,
    networkDown: 0,
    uptime: 0,
};