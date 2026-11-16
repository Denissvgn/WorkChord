import { lazy, Suspense } from 'react';
import { LoaderCircle } from 'lucide-react';
import { Route, Routes } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { BareLayout } from './components/layout/BareLayout';
import { LegacyRedirect } from './navigation/LegacyRedirect';
import { AppShell } from './components/layout/AppShell';
import { DocumentMetadata } from './components/layout/DocumentMetadata';
import { routeModuleLoaders } from './navigation/routeModules';

const OverviewPage = lazy(routeModuleLoaders.overview);
const LandingPage = lazy(routeModuleLoaders.landing);
const PlanPage = lazy(routeModuleLoaders.plan);
const PlanSharePage = lazy(routeModuleLoaders.planShare);
const CalendarPage = lazy(routeModuleLoaders.calendar);
const IterationsPage = lazy(routeModuleLoaders.iterations);
const TeamPage = lazy(routeModuleLoaders.team);
const TasksPage = lazy(routeModuleLoaders.tasks);
const MyWorkPage = lazy(routeModuleLoaders.myWork);
const NativeConnectionPage = lazy(routeModuleLoaders.nativeConnection);
const TriagePage = lazy(routeModuleLoaders.triage);
const ProjectsPage = lazy(routeModuleLoaders.projects);
const ProjectDetailPage = lazy(routeModuleLoaders.projectDetail);
const ProjectReleaseDetailPage = lazy(routeModuleLoaders.projectReleaseDetail);
const GanttPage = lazy(routeModuleLoaders.gantt);
const AnalyticsPage = lazy(routeModuleLoaders.analytics);
const SettingsPage = lazy(routeModuleLoaders.settings);
const AgentPipelinePage = lazy(routeModuleLoaders.agentPipeline);
const AgentTeamSetupMasterPage = lazy(routeModuleLoaders.agentTeamSetup);
const NotFoundPage = lazy(routeModuleLoaders.notFound);

export const RouteLoadingState = () => {
  const { t } = useTranslation();
  return (
    <div
      className="flex min-h-64 items-center justify-center gap-3 text-content-secondary"
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <LoaderCircle aria-hidden="true" className="h-5 w-5 animate-spin text-action" />
      <span>{t('routeLoading.message')}</span>
    </div>
  );
};

const WorkspaceRoutes = () => (
  <Routes>
    <Route path="/" element={<OverviewPage />} />
    <Route path="/plan" element={<PlanPage />} />
    <Route path="/plan/master" element={<LegacyRedirect><PlanPage /></LegacyRedirect>} />
    <Route path="/calendar" element={<LegacyRedirect><CalendarPage /></LegacyRedirect>} />
    <Route path="/iterations" element={<LegacyRedirect><IterationsPage /></LegacyRedirect>} />
    <Route path="/team" element={<TeamPage />} />
    <Route path="/tasks" element={<TasksPage />} />
    <Route path="/my-work" element={<MyWorkPage />} />
    <Route path="/triage" element={<TriagePage />} />
    <Route path="/projects" element={<ProjectsPage />} />
    <Route path="/projects/:projectId" element={<ProjectDetailPage />} />
    <Route path="/projects/:projectId/releases/:releaseId" element={<ProjectReleaseDetailPage />} />
    <Route path="/roadmap" element={<LegacyRedirect><ProjectsPage /></LegacyRedirect>} />
    <Route path="/gantt" element={<GanttPage />} />
    <Route path="/analytics" element={<AnalyticsPage />} />
    <Route path="/settings" element={<SettingsPage />} />
    <Route path="/agent-pipeline" element={<LegacyRedirect><AgentPipelinePage /></LegacyRedirect>} />
    <Route path="/agent-team/setup" element={<LegacyRedirect><AgentTeamSetupMasterPage /></LegacyRedirect>} />
    <Route path="*" element={<NotFoundPage />} />
  </Routes>
);

const WorkspaceApp = () => (
  <AppShell>
    <Suspense fallback={<RouteLoadingState />}>
      <WorkspaceRoutes />
    </Suspense>
  </AppShell>
);

const LandingRoute = () => (
  <>
    <DocumentMetadata />
    <Suspense fallback={<RouteLoadingState />}>
      <LandingPage />
    </Suspense>
  </>
);

function App() {
  return (
    <Routes>
      <Route path="/plan/share/:publicId" element={<BareLayout><Suspense fallback={<RouteLoadingState />}><PlanSharePage /></Suspense></BareLayout>} />
      <Route path="/mobile/connect" element={<BareLayout><Suspense fallback={<RouteLoadingState />}><NativeConnectionPage /></Suspense></BareLayout>} />
      <Route path="/welcome" element={<LandingRoute />} />
      <Route path="*" element={<WorkspaceApp />} />
    </Routes>
  );
}

export default App;
