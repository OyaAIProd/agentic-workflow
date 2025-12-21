-- Agentic Workflow - Memory Persistence Schema
-- PostgreSQL schema for AI agent memory
-- Author: Julien GELEE
-- License: MIT

-- Sessions table - Track conversation sessions
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    summary TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Actions table - Log all significant actions
CREATE TABLE IF NOT EXISTS actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id),
    action_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    target_path TEXT,
    status VARCHAR(50) DEFAULT 'completed',
    metadata JSONB DEFAULT '{}'::jsonb,
    keywords TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Error solutions table - Learn from mistakes
CREATE TABLE IF NOT EXISTS error_solutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    error_type VARCHAR(200) NOT NULL,
    error_message TEXT NOT NULL,
    solution TEXT NOT NULL,
    related_files TEXT[],
    solution_worked BOOLEAN DEFAULT NULL,
    occurrences INTEGER DEFAULT 1,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Context table - Key-value store for project context
CREATE TABLE IF NOT EXISTS context (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key VARCHAR(200) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    category VARCHAR(100) DEFAULT 'general',
    importance INTEGER DEFAULT 5 CHECK (importance >= 1 AND importance <= 10),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Knowledge base table - Accumulated knowledge
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic VARCHAR(300) NOT NULL,
    content TEXT NOT NULL,
    source VARCHAR(200),
    confidence DECIMAL(3,2) DEFAULT 0.80 CHECK (confidence >= 0 AND confidence <= 1),
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Checkpoints table - Save progress milestones
CREATE TABLE IF NOT EXISTS checkpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    is_milestone BOOLEAN DEFAULT FALSE,
    state JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_actions_type ON actions(action_type);
CREATE INDEX IF NOT EXISTS idx_actions_created ON actions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_error_solutions_type ON error_solutions(error_type);
CREATE INDEX IF NOT EXISTS idx_context_key ON context(key);
CREATE INDEX IF NOT EXISTS idx_context_category ON context(category);
CREATE INDEX IF NOT EXISTS idx_knowledge_tags ON knowledge_base USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_checkpoints_milestone ON checkpoints(is_milestone);

-- Full text search on knowledge base
CREATE INDEX IF NOT EXISTS idx_knowledge_fts ON knowledge_base
    USING GIN(to_tsvector('english', topic || ' ' || content));
