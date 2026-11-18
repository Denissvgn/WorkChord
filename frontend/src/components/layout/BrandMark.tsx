/**
 * WorkChord logo for the top bar: one ring crossed by a chord of hexagon
 * cells. It is the same drawing as `public/favicon.svg`, so the header and
 * the browser tab show the same mark.
 */
export function BrandMark() {
    return (
        <div className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
                <rect width="512" height="512" rx="112" fill="#18305B" />
                <g fill="none" stroke="#FFFFFF" strokeOpacity="0.85" strokeWidth="52" strokeLinecap="round">
                    <path d="M420.59 222.32A168 168 0 0 1 194.26 412.24" />
                    <path d="M91.41 289.68A168 168 0 0 1 317.74 99.76" />
                </g>
                <g strokeLinejoin="round" strokeWidth="16">
                    <polygon points="188.14,348.18 169.68,398.93 116.5,408.3 81.79,366.94 100.25,316.19 153.43,306.82" fill="#FFFFFF" stroke="#FFFFFF" />
                    <polygon points="346.6,240.02 315.14,326.48 224.53,342.45 165.4,271.98 196.86,185.52 287.47,169.55" fill="#3B82F6" stroke="#3B82F6" />
                    <polygon points="430.21,145.06 411.75,195.81 358.57,205.18 323.86,163.82 342.32,113.07 395.5,103.7" fill="#FFFFFF" stroke="#FFFFFF" />
                </g>
            </svg>
        </div>
    );
}
