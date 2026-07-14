import { Component, type ErrorInfo, type ReactNode } from 'react';
import { AlertTriangle, Home, RefreshCw } from 'lucide-react';
import { Button } from '../common/Button';

interface RouteErrorBoundaryProps {
    children: ReactNode;
    resetKey: string;
    title: string;
    description: string;
    refreshLabel: string;
    homeLabel: string;
}

interface RouteErrorBoundaryState {
    error: Error | null;
}

export class RouteErrorBoundary extends Component<RouteErrorBoundaryProps, RouteErrorBoundaryState> {
    state: RouteErrorBoundaryState = { error: null };

    static getDerivedStateFromError(error: Error): RouteErrorBoundaryState {
        return { error };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Route render failed:', error, errorInfo);
    }

    componentDidUpdate(previousProps: RouteErrorBoundaryProps) {
        if (previousProps.resetKey !== this.props.resetKey && this.state.error) {
            this.setState({ error: null });
        }
    }

    render() {
        if (!this.state.error) {
            return this.props.children;
        }

        return (
            <div className="m-4 rounded-lg border border-feedback-danger-border bg-feedback-danger-muted p-6 text-feedback-danger-foreground" role="alert">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
                    <AlertTriangle className="h-6 w-6 shrink-0 text-feedback-danger" />
                    <div className="min-w-0 flex-1">
                        <h1 className="text-xl font-semibold">{this.props.title}</h1>
                        <p className="mt-2 text-sm text-feedback-danger-foreground">
                            {this.props.description}
                        </p>
                        <div className="mt-4 flex flex-wrap gap-2">
                            <Button variant="secondary" onClick={() => window.location.reload()}>
                                <RefreshCw aria-hidden="true" className="mr-2 h-4 w-4" />
                                {this.props.refreshLabel}
                            </Button>
                            <Button variant="outline" onClick={() => window.location.assign('/')}>
                                <Home aria-hidden="true" className="mr-2 h-4 w-4" />
                                {this.props.homeLabel}
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
