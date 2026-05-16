import React, { useEffect, useState } from 'react';
import OverlayContainer from './components/OverlayContainer';
import ArcReactor from './components/ArcReactor';
import TaskSurface from './components/TaskSurface';
import TransitionManager from './components/TransitionManager';
import BootSplash from './components/BootSplash';
import NotificationToast from './components/NotificationToast';
import { useVoiceState } from './hooks/useVoiceState';
import { useTaskSurface } from './hooks/useTaskSurface';
import { useTransition } from './hooks/useTransition';
import { uiStore } from './store/uiStore';

const App: React.FC = () => {
    const [booted, setBooted] = useState(false);
    const voiceState = useVoiceState();
    const { activeTask, openTask, closeTask } = useTaskSurface();
    const { transitioning } = useTransition();

    useEffect(() => {
        const timer = setTimeout(() => setBooted(true), 2000);
        return () => clearTimeout(timer);
    }, []);

    if (!booted) {
        return <BootSplash />;
    }

    return (
        <OverlayContainer>
            <ArcReactor voiceState={voiceState} />
            {activeTask && (
                <TaskSurface taskType={activeTask} onClose={closeTask} />
            )}
            <TransitionManager active={transitioning} />
            <NotificationToast />
        </OverlayContainer>
    );
};

export default App;