import {
useEffect,
useMemo,
useState,
} from "react";

import {
getEmbeddingPoints,
getQueryVisualization,
} from "../../services/api";

import "./EmbeddingSpace.css";

const WIDTH = 1000;
const HEIGHT = 520;
const PADDING = 55;

const COLORS = [
"#818cf8",
"#34d399",
"#fbbf24",
"#f87171",
"#22d3ee",
"#f472b6",
"#a78bfa",
"#2dd4bf",
];

function scale(
value,
min,
max,
outputMin,
outputMax
) {
if (max === min) {
return (
(outputMin + outputMax) / 2
);
}

return (
    outputMin +
    ((value - min) / (max - min)) *
        (outputMax - outputMin)
);


}

function truncateText(
text,
length = 100
) {
if (!text) {
return "";
}

return text.length > length
    ? `${text.slice(0, length)}...`
    : text;
}

export default function EmbeddingSpace({
mode = "documents",
question: externalQuestion = "",
documentIds = null,
}) {
const isQueryMode =
mode === "query";

// --------------------------------------------------
// Base embedding data
// --------------------------------------------------

const [points, setPoints] =
    useState([]);

const [loading, setLoading] =
    useState(true);

const [error, setError] =
    useState(null);


// --------------------------------------------------
// Query visualization
// --------------------------------------------------

const [queryData, setQueryData] =
    useState(null);

const [queryLoading, setQueryLoading] =
    useState(false);

const [queryError, setQueryError] =
    useState(null);


// --------------------------------------------------
// UI state
// --------------------------------------------------

const [selectedPoint, setSelectedPoint] =
    useState(null);

const [hoveredPoint, setHoveredPoint] =
    useState(null);

const [selectedDocument, setSelectedDocument] =
    useState("all");

const [searchText, setSearchText] =
    useState("");

const [zoom, setZoom] =
    useState(1);


// --------------------------------------------------
// Load stored embedding points
// --------------------------------------------------

useEffect(() => {
    async function loadPoints() {
        try {
            setLoading(true);
            setError(null);

            const data =
                await getEmbeddingPoints(
                    documentIds
                );

            setPoints(
                data.points || []
            );
        } catch (err) {
            console.error(
                "Failed to load embedding points:",
                err
            );

            setError(
                err.message ||
                    "Failed to load embedding data."
            );
        } finally {
            setLoading(false);
        }
    }

    loadPoints();
}, [documentIds]);


// --------------------------------------------------
// Reset visualization state when switching modes
// --------------------------------------------------

useEffect(() => {
    setQueryData(null);
    setQueryError(null);
    setSelectedPoint(null);
    setHoveredPoint(null);
    setSelectedDocument("all");
    setSearchText("");
    setZoom(1);
}, [mode]);


// --------------------------------------------------
// Automatically visualize supplied question
// --------------------------------------------------

useEffect(() => {
    if (!isQueryMode) {
        return;
    }

    if (
        !externalQuestion ||
        !externalQuestion.trim()
    ) {
        return;
    }

    visualizeExternalQuestion(
        externalQuestion.trim()
    );
}, [
    externalQuestion,
    isQueryMode,
]);


// --------------------------------------------------
// Visualize externally supplied question
// --------------------------------------------------

async function visualizeExternalQuestion(
    questionToVisualize
) {
    try {
        setQueryLoading(true);
        setQueryError(null);
        setSelectedPoint(null);

        const ids =
            documentIds &&
            documentIds.length > 0
                ? documentIds
                : null;

        const data =
            await getQueryVisualization(
                questionToVisualize,
                ids,
                5
            );

        setQueryData(data);
    } catch (err) {
        console.error(
            "Failed to visualize conversation question:",
            err
        );

        setQueryError(
            err.message ||
                "Failed to visualize query."
        );
    } finally {
        setQueryLoading(false);
    }
}


// --------------------------------------------------
// Documents
// --------------------------------------------------

const documents = useMemo(() => {
    const documentMap =
        new Map();

    points.forEach((point) => {
        if (
            !documentMap.has(
                point.document_id
            )
        ) {
            documentMap.set(
                point.document_id,
                {
                    id: point.document_id,
                    source: point.source,
                    count: 0,
                }
            );
        }

        documentMap.get(
            point.document_id
        ).count += 1;
    });

    return Array.from(
        documentMap.values()
    );
}, [points]);


// --------------------------------------------------
// Points currently displayed
// --------------------------------------------------

const visualizationPoints =
    isQueryMode && queryData
        ? queryData.points || []
        : points;


// --------------------------------------------------
// Bounds
// --------------------------------------------------

const bounds = useMemo(() => {
    if (
        visualizationPoints.length === 0
    ) {
        return null;
    }

    const xs =
        visualizationPoints.map(
            (point) => point.x
        );

    const ys =
        visualizationPoints.map(
            (point) => point.y
        );

    if (
        isQueryMode &&
        queryData?.query
    ) {
        xs.push(
            queryData.query.x
        );

        ys.push(
            queryData.query.y
        );
    }

    return {
        minX: Math.min(...xs),
        maxX: Math.max(...xs),
        minY: Math.min(...ys),
        maxY: Math.max(...ys),
    };
}, [
    visualizationPoints,
    queryData,
    isQueryMode,
]);


// --------------------------------------------------
// Filter points
// --------------------------------------------------

const filteredPoints =
    useMemo(() => {
        return visualizationPoints.filter(
            (point) => {
                const matchesDocument =
                    selectedDocument ===
                        "all" ||
                    String(
                        point.document_id
                    ) ===
                        selectedDocument;

                const search =
                    searchText
                        .trim()
                        .toLowerCase();

                if (!search) {
                    return matchesDocument;
                }

                const searchableText = [
                    point.source,
                    point.content,
                    point.page,
                    point.chunk_index,
                    point.id,
                ]
                    .join(" ")
                    .toLowerCase();

                return (
                    matchesDocument &&
                    searchableText.includes(
                        search
                    )
                );
            }
        );
    }, [
        visualizationPoints,
        selectedDocument,
        searchText,
    ]);


// --------------------------------------------------
// Document colors
// --------------------------------------------------

const documentColorMap =
    useMemo(() => {
        const map =
            new Map();

        documents.forEach(
            (document, index) => {
                map.set(
                    document.id,
                    COLORS[
                        index %
                            COLORS.length
                    ]
                );
            }
        );

        return map;
    }, [documents]);


function getPointColor(
    documentId
) {
    return (
        documentColorMap.get(
            documentId
        ) || COLORS[0]
    );
}


// --------------------------------------------------
// Coordinates
// --------------------------------------------------

function getCoordinates(point) {
    if (!bounds) {
        return {
            x: WIDTH / 2,
            y: HEIGHT / 2,
        };
    }

    const baseX =
        scale(
            point.x,
            bounds.minX,
            bounds.maxX,
            PADDING,
            WIDTH - PADDING
        );

    const baseY =
        scale(
            point.y,
            bounds.minY,
            bounds.maxY,
            HEIGHT - PADDING,
            PADDING
        );

    const centerX =
        WIDTH / 2;

    const centerY =
        HEIGHT / 2;

    return {
        x:
            centerX +
            (baseX - centerX) *
                zoom,

        y:
            centerY +
            (baseY - centerY) *
                zoom,
    };
}


// --------------------------------------------------
// Zoom
// --------------------------------------------------

function resetView() {
    setZoom(1);
}


function zoomIn() {
    setZoom((current) =>
        Math.min(
            current + 0.1,
            3
        )
    );
}


function zoomOut() {
    setZoom((current) =>
        Math.max(
            current - 0.1,
            0.7
        )
    );
}


function handleWheel(event) {
    event.preventDefault();

    const direction =
        event.deltaY < 0
            ? 1
            : -1;

    setZoom((current) => {
        const next =
            current +
            direction * 0.05;

        return Math.min(
            Math.max(
                next,
                0.7
            ),
            3
        );
    });
}


// --------------------------------------------------
// Loading state
// --------------------------------------------------

if (loading) {
    return (
        <section className="embedding-space">

            <div className="embedding-loading">

                <div className="loading-spinner" />

                <strong>
                    Loading embedding space
                </strong>

                <span>
                    Reading chunk embeddings
                    from PostgreSQL...
                </span>

            </div>

        </section>
    );
}


// --------------------------------------------------
// Query loading state
// --------------------------------------------------

if (
    isQueryMode &&
    queryLoading
) {
    return (
        <section className="embedding-space">

            <div className="embedding-loading">

                <div className="loading-spinner" />

                <strong>
                    Visualizing query
                </strong>

                <span>
                    Finding the position of
                    the question and retrieved
                    chunks...
                </span>

            </div>

        </section>
    );
}


// --------------------------------------------------
// Error state
// --------------------------------------------------

if (error) {
    return (
        <section className="embedding-space">

            <div className="embedding-error">

                <strong>
                    Unable to load embedding
                    visualization
                </strong>

                <span>
                    {error}
                </span>

                <button
                    type="button"
                    onClick={() =>
                        window.location.reload()
                    }
                >
                    Retry
                </button>

            </div>

        </section>
    );
}


// --------------------------------------------------
// Query error
// --------------------------------------------------

if (
    isQueryMode &&
    queryError
) {
    return (
        <section className="embedding-space">

            <div className="embedding-error">

                <strong>
                    Unable to visualize query
                </strong>

                <span>
                    {queryError}
                </span>

            </div>

        </section>
    );
}


// --------------------------------------------------
// Empty state
// --------------------------------------------------

if (
    !bounds ||
    visualizationPoints.length === 0
) {
    return (
        <section className="embedding-space">

            <div className="embedding-empty">
                No embedding points are
                available.
            </div>

        </section>
    );
}


// --------------------------------------------------
// Main UI
//
// IMPORTANT SCROLL STRUCTURE:
//
// embedding-space
//     ├── header
//     ├── query summary
//     ├── toolbar
//     └── embedding-main
//             ├── chart
//             └── sidebar  ← ONLY SCROLL AREA
//
// This keeps the header, toolbar and graph fixed
// while the complete right-side information panel
// scrolls as one unit.
// --------------------------------------------------

return (
    <section className="embedding-space">

        {/* ---------------------------------------- */}
        {/* Fixed Header */}
        {/* ---------------------------------------- */}

        <div className="embedding-header">

            <div>

                <div className="embedding-title-row">

                    <h2>
                        {isQueryMode
                            ? "Query Embedding Visualization"
                            : "Embedding Space Explorer"}
                    </h2>

                    <span className="live-badge">
                        LIVE DATA
                    </span>

                </div>

                <p>
                    {isQueryMode
                        ? "See how the conversation question relates to the stored document chunks."
                        : "Explore how your document chunks are distributed in the embedding space."}
                </p>

            </div>


            <div className="embedding-stats">

                <div className="stat-card">

                    <strong>
                        {visualizationPoints.length}
                    </strong>

                    <span>
                        Chunks
                    </span>

                </div>


                <div className="stat-card">

                    <strong>
                        {documents.length}
                    </strong>

                    <span>
                        Documents
                    </span>

                </div>


                <div className="stat-card">

                    <strong>
                        {filteredPoints.length}
                    </strong>

                    <span>
                        Visible
                    </span>

                </div>

            </div>

        </div>


        {/* ---------------------------------------- */}
        {/* Query Summary */}
        {/* ---------------------------------------- */}

        {isQueryMode &&
            queryData?.query && (

            <div className="query-result-summary">

                <div className="query-result-question">

                    <span>
                        Query
                    </span>

                    <strong>
                        "{queryData.query.question}"
                    </strong>

                </div>


                <div className="query-result-stat">

                    <strong>
                        {queryData.retrieved_count}
                    </strong>

                    <span>
                        Retrieved chunks
                    </span>

                </div>


                <div className="query-legend">

                    <span>
                        <i className="legend-query" />
                        Query
                    </span>

                    <span>
                        <i className="legend-retrieved" />
                        Retrieved
                    </span>

                    <span>
                        <i className="legend-chunk" />
                        Other chunks
                    </span>

                </div>

            </div>
        )}


        {/* ---------------------------------------- */}
        {/* Fixed Toolbar */}
        {/* ---------------------------------------- */}

        <div className="embedding-toolbar">

            <div className="toolbar-group">

                <label htmlFor="document-filter">
                    Document
                </label>

                <select
                    id="document-filter"
                    value={selectedDocument}
                    onChange={(event) => {
                        setSelectedDocument(
                            event.target.value
                        );

                        setSelectedPoint(
                            null
                        );
                    }}
                >

                    <option value="all">
                        All documents
                    </option>

                    {documents.map(
                        (document) => (
                            <option
                                key={
                                    document.id
                                }
                                value={
                                    document.id
                                }
                            >
                                {document.source}
                                {" "}
                                (
                                {document.count}
                                )
                            </option>
                        )
                    )}

                </select>

            </div>


            <div className="toolbar-search">

                <span>
                    ⌕
                </span>

                <input
                    type="text"
                    placeholder="Search chunks..."
                    value={searchText}
                    onChange={(event) => {
                        setSearchText(
                            event.target.value
                        );

                        setSelectedPoint(
                            null
                        );
                    }}
                />

                {searchText && (
                    <button
                        type="button"
                        onClick={() =>
                            setSearchText("")
                        }
                        aria-label="Clear search"
                    >
                        ×
                    </button>
                )}

            </div>


            <div className="zoom-controls">

                <button
                    type="button"
                    onClick={zoomOut}
                    title="Zoom out"
                >
                    −
                </button>

                <span>
                    {Math.round(
                        zoom * 100
                    )}
                    %
                </span>

                <button
                    type="button"
                    onClick={zoomIn}
                    title="Zoom in"
                >
                    +
                </button>

                <button
                    type="button"
                    onClick={resetView}
                    title="Reset zoom"
                >
                    Reset
                </button>

            </div>

        </div>


        {/* ---------------------------------------- */}
        {/* Main Fixed Visualization Area */}
        {/* ---------------------------------------- */}

        <div className="embedding-main">


            {/* ---------------------------------- */}
            {/* Fixed Graph */}
            {/* ---------------------------------- */}

            <div className="embedding-chart-card">

                <div className="chart-help">

                    <span>
                        Scroll to zoom
                    </span>

                    <span>
                        Click a point for details
                    </span>

                </div>


                <div
                    className="embedding-svg-container"
                    onWheel={handleWheel}
                >

                    <svg
                        className="embedding-chart"
                        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
                    >

                        <defs>

                            <pattern
                                id="embedding-grid"
                                width="40"
                                height="40"
                                patternUnits="userSpaceOnUse"
                            >

                                <path
                                    d="M 40 0 L 0 0 0 40"
                                    className="grid-line"
                                    fill="none"
                                />

                            </pattern>

                        </defs>


                        <rect
                            x="0"
                            y="0"
                            width={WIDTH}
                            height={HEIGHT}
                            className="chart-background"
                        />


                        <rect
                            x={PADDING}
                            y={PADDING}
                            width={
                                WIDTH -
                                PADDING * 2
                            }
                            height={
                                HEIGHT -
                                PADDING * 2
                            }
                            fill="url(#embedding-grid)"
                        />


                        <line
                            x1={
                                WIDTH / 2
                            }
                            y1={PADDING}
                            x2={
                                WIDTH / 2
                            }
                            y2={
                                HEIGHT -
                                PADDING
                            }
                            className="center-axis"
                        />


                        <line
                            x1={PADDING}
                            y1={
                                HEIGHT / 2
                            }
                            x2={
                                WIDTH -
                                PADDING
                            }
                            y2={
                                HEIGHT / 2
                            }
                            className="center-axis"
                        />


                        {/* -------------------------------- */}
                        {/* Document Chunks */}
                        {/* -------------------------------- */}

                        {filteredPoints.map(
                            (point) => {

                                const {
                                    x,
                                    y,
                                } =
                                    getCoordinates(
                                        point
                                    );

                                const isSelected =
                                    selectedPoint?.id ===
                                    point.id;

                                const isHovered =
                                    hoveredPoint?.id ===
                                    point.id;

                                const isRetrieved =
                                    Boolean(
                                        isQueryMode &&
                                        queryData &&
                                        point.retrieved
                                    );

                                return (
                                    <g
                                        key={
                                            point.id
                                        }
                                    >

                                        {isRetrieved && (
                                            <circle
                                                cx={x}
                                                cy={y}
                                                r={12}
                                                className="retrieved-glow"
                                            />
                                        )}


                                        {(isSelected ||
                                            isHovered) && (
                                            <circle
                                                cx={x}
                                                cy={y}
                                                r={12}
                                                fill="none"
                                                stroke={
                                                    isRetrieved
                                                        ? "#22c55e"
                                                        : getPointColor(
                                                            point.document_id
                                                        )
                                                }
                                                strokeWidth="2"
                                                opacity="0.5"
                                            />
                                        )}


                                        <circle
                                            cx={x}
                                            cy={y}
                                            r={
                                                isSelected
                                                    ? 7
                                                    : isHovered
                                                    ? 6
                                                    : isRetrieved
                                                    ? 6
                                                    : 4.5
                                            }
                                            fill={
                                                isRetrieved
                                                    ? "#22c55e"
                                                    : getPointColor(
                                                        point.document_id
                                                    )
                                            }
                                            className="embedding-point"
                                            opacity={
                                                isSelected ||
                                                isHovered ||
                                                isRetrieved
                                                    ? 1
                                                    : 0.72
                                            }
                                            onMouseEnter={() =>
                                                setHoveredPoint(
                                                    point
                                                )
                                            }
                                            onMouseLeave={() =>
                                                setHoveredPoint(
                                                    null
                                                )
                                            }
                                            onClick={(
                                                event
                                            ) => {
                                                event.stopPropagation();

                                                setSelectedPoint(
                                                    point
                                                );
                                            }}
                                        />

                                    </g>
                                );
                            }
                        )}


                        {/* -------------------------------- */}
                        {/* Query Point */}
                        {/* -------------------------------- */}

                        {isQueryMode &&
                            queryData?.query && (
                            (() => {
                                const {
                                    x,
                                    y,
                                } =
                                    getCoordinates(
                                        queryData.query
                                    );

                                return (
                                    <g
                                        className="query-point-group"
                                    >

                                        <circle
                                            cx={x}
                                            cy={y}
                                            r={18}
                                            className="query-point-glow"
                                        />

                                        <circle
                                            cx={x}
                                            cy={y}
                                            r={9}
                                            className="query-point"
                                        />

                                        <circle
                                            cx={x}
                                            cy={y}
                                            r={4}
                                            className="query-point-core"
                                        />

                                        <text
                                            x={
                                                x + 14
                                            }
                                            y={
                                                y - 14
                                            }
                                            className="query-point-label"
                                        >
                                            Query
                                        </text>

                                    </g>
                                );
                            })()
                        )}


                        <text
                            x={
                                WIDTH -
                                PADDING
                            }
                            y={
                                HEIGHT - 18
                            }
                            className="axis-label"
                            textAnchor="end"
                        >
                            PCA Component 1
                        </text>


                        <text
                            x={20}
                            y={PADDING}
                            className="axis-label"
                        >
                            PCA Component 2
                        </text>

                    </svg>


                    {/* -------------------------------- */}
                    {/* Hover Tooltip */}
                    {/* -------------------------------- */}

                    {hoveredPoint && (
                        <div className="point-tooltip">

                            <strong>
                                {
                                    hoveredPoint.source
                                }
                            </strong>

                            <span>
                                Page{" "}
                                {
                                    hoveredPoint.page
                                }
                                {" "}
                                · Chunk{" "}
                                {
                                    hoveredPoint.chunk_index
                                }
                            </span>


                            {isQueryMode &&
                                hoveredPoint.retrieved && (
                                <span className="tooltip-retrieved">
                                    ✓ Retrieved for this query
                                </span>
                            )}


                            {isQueryMode &&
                                hoveredPoint.distance !==
                                    null &&
                                hoveredPoint.distance !==
                                    undefined && (
                                <span>
                                    Vector distance:{" "}
                                    {
                                        hoveredPoint.distance.toFixed(
                                            4
                                        )
                                    }
                                </span>
                            )}


                            <p>
                                {truncateText(
                                    hoveredPoint.content
                                )}
                            </p>

                        </div>
                    )}

                </div>

            </div>


            {/* ---------------------------------- */}
            {/* Scrollable Right Information Panel */}
            {/* ---------------------------------- */}

            <aside className="embedding-sidebar">

                {/* Documents */}

                <div className="sidebar-section">

                    <h3>
                        Documents
                    </h3>


                    <div className="document-list">

                        {documents.map(
                            (document) => {

                                const active =
                                    selectedDocument ===
                                        "all" ||
                                    String(
                                        document.id
                                    ) ===
                                        selectedDocument;

                                return (
                                    <button
                                        type="button"
                                        key={
                                            document.id
                                        }
                                        className={
                                            active
                                                ? "document-legend active"
                                                : "document-legend"
                                        }
                                        onClick={() =>
                                            setSelectedDocument(
                                                String(
                                                    document.id
                                                )
                                            )
                                        }
                                    >

                                        <span
                                            className="legend-color"
                                            style={{
                                                background:
                                                    getPointColor(
                                                        document.id
                                                    ),
                                            }}
                                        />


                                        <span className="document-name">
                                            {
                                                document.source
                                            }
                                        </span>


                                        <span className="document-count">
                                            {
                                                document.count
                                            }
                                        </span>

                                    </button>
                                );
                            }
                        )}

                    </div>

                </div>


                {/* Query Results */}

                {isQueryMode &&
                    queryData && (
                    <div className="sidebar-section">

                        <div className="selected-heading">

                            <h3>
                                Retrieved Chunks
                            </h3>

                        </div>


                        <div className="retrieved-list">

                            {queryData.points
                                .filter(
                                    (point) =>
                                        point.retrieved
                                )
                                .sort(
                                    (a, b) =>
                                        a.distance -
                                        b.distance
                                )
                                .map(
                                    (point) => (
                                        <button
                                            type="button"
                                            key={
                                                point.id
                                            }
                                            className="retrieved-item"
                                            onClick={() =>
                                                setSelectedPoint(
                                                    point
                                                )
                                            }
                                        >

                                            <div>

                                                <strong>
                                                    Page{" "}
                                                    {
                                                        point.page
                                                    }
                                                    {" "}
                                                    · Chunk{" "}
                                                    {
                                                        point.chunk_index
                                                    }
                                                </strong>

                                                <span>
                                                    Distance{" "}
                                                    {
                                                        point.distance.toFixed(
                                                            4
                                                        )
                                                    }
                                                </span>

                                            </div>


                                            <p>
                                                {
                                                    truncateText(
                                                        point.content,
                                                        80
                                                    )
                                                }
                                            </p>

                                        </button>
                                    )
                                )}

                        </div>

                    </div>
                )}


                {/* About */}

                <div className="sidebar-section">

                    <h3>
                        About this view
                    </h3>


                    <div className="info-box">

                        <div>

                            <strong>
                                PCA
                            </strong>

                            <span>
                                High-dimensional
                                embeddings reduced
                                to 2D.
                            </span>

                        </div>


                        <div>

                            <strong>
                                Point
                            </strong>

                            <span>
                                One point represents
                                one stored document
                                chunk.
                            </span>

                        </div>


                        {isQueryMode ? (
                            <>

                                <div>

                                    <strong>
                                        Query
                                    </strong>

                                    <span>
                                        The highlighted
                                        query point is
                                        the embedding of
                                        the conversation
                                        question.
                                    </span>

                                </div>


                                <div>

                                    <strong>
                                        Retrieved
                                    </strong>

                                    <span>
                                        Green points are
                                        the chunks returned
                                        for this query.
                                    </span>

                                </div>

                            </>
                        ) : (
                            <div>

                                <strong>
                                    Documents
                                </strong>

                                <span>
                                    Each document is
                                    represented by its
                                    stored chunk
                                    embeddings.
                                </span>

                            </div>
                        )}

                    </div>

                </div>


                {/* Selected Chunk */}

                {selectedPoint && (
                    <div className="sidebar-section selected-section">

                        <div className="selected-heading">

                            <h3>
                                Selected Chunk
                            </h3>

                            <button
                                type="button"
                                onClick={() =>
                                    setSelectedPoint(
                                        null
                                    )
                                }
                                aria-label="Close selected chunk"
                                title="Close"
                            >
                                ×
                            </button>

                        </div>


                        <div className="selected-meta">

                            <div>

                                <span>
                                    Document
                                </span>

                                <strong>
                                    {
                                        selectedPoint.source
                                    }
                                </strong>

                            </div>


                            <div>

                                <span>
                                    Page
                                </span>

                                <strong>
                                    {
                                        selectedPoint.page
                                    }
                                </strong>

                            </div>


                            <div>

                                <span>
                                    Chunk
                                </span>

                                <strong>
                                    {
                                        selectedPoint.chunk_index
                                    }
                                </strong>

                            </div>


                            <div>

                                <span>
                                    ID
                                </span>

                                <strong>
                                    {
                                        selectedPoint.id
                                    }
                                </strong>

                            </div>


                            {isQueryMode &&
                                selectedPoint.distance !==
                                    null &&
                                selectedPoint.distance !==
                                    undefined && (
                                <div>

                                    <span>
                                        Distance
                                    </span>

                                    <strong>
                                        {
                                            selectedPoint.distance.toFixed(
                                                4
                                            )
                                        }
                                    </strong>

                                </div>
                            )}

                        </div>


                        <div className="chunk-content">

                            {
                                selectedPoint.content
                            }

                        </div>

                    </div>
                )}

            </aside>

        </div>

    </section>
);

}
