import type { VersionDiffResponse, DiffLineResponse } from '../../types';

interface Props {
  diff: VersionDiffResponse;
}

export function DiffViewer({ diff }: Props) {
  if (!diff.has_changes) {
    return (
      <div className="flex flex-col items-center justify-center py-12 gap-2 text-center">
        <div className="w-10 h-10 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
          <svg className="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Versões idênticas</p>
        <p className="text-xs text-gray-500 dark:text-gray-400">Não há diferenças entre as versões selecionadas.</p>
      </div>
    );
  }

  const stats = diff.lines.reduce(
    (acc, l) => {
      if (l.kind === 'insert') acc.added++;
      else if (l.kind === 'delete') acc.removed++;
      return acc;
    },
    { added: 0, removed: 0 }
  );

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-3 text-xs font-medium">
        <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
          <span className="font-mono">+{stats.added}</span>
          <span className="text-gray-400 dark:text-gray-500 font-normal">adições</span>
        </span>
        <span className="flex items-center gap-1 text-red-500 dark:text-red-400">
          <span className="font-mono">-{stats.removed}</span>
          <span className="text-gray-400 dark:text-gray-500 font-normal">remoções</span>
        </span>
        <span className="ml-auto text-gray-400 dark:text-gray-500 font-normal">
          v{diff.version_number_before} → v{diff.version_number_after}
        </span>
      </div>

      <div className="rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div className="flex text-xs font-medium bg-gray-100 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <div className="w-12 shrink-0 px-3 py-2 text-gray-500 dark:text-gray-400 text-center border-r border-gray-200 dark:border-gray-700">
            base
          </div>
          <div className="w-12 shrink-0 px-3 py-2 text-gray-500 dark:text-gray-400 text-center border-r border-gray-200 dark:border-gray-700">
            nova
          </div>
          <div className="flex-1 px-4 py-2 text-gray-500 dark:text-gray-400">conteúdo</div>
        </div>

        <div className="overflow-x-auto">
          <div className="min-w-0">
            {diff.lines.map((line, idx) => (
              <DiffLine key={idx} line={line} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function DiffLine({ line }: { line: DiffLineResponse }) {
  const isInsert = line.kind === 'insert';
  const isDelete = line.kind === 'delete';

  const rowClass = isInsert
    ? 'bg-emerald-50 dark:bg-emerald-950/30'
    : isDelete
    ? 'bg-red-50 dark:bg-red-950/30'
    : '';

  const gutterClass = isInsert
    ? 'bg-emerald-100/70 dark:bg-emerald-900/30 border-emerald-200 dark:border-emerald-800'
    : isDelete
    ? 'bg-red-100/70 dark:bg-red-900/30 border-red-200 dark:border-red-800'
    : 'bg-gray-50 dark:bg-gray-900 border-gray-100 dark:border-gray-800';

  const prefixClass = isInsert
    ? 'text-emerald-600 dark:text-emerald-400 font-bold'
    : isDelete
    ? 'text-red-500 dark:text-red-400 font-bold'
    : 'text-gray-300 dark:text-gray-600';

  const contentClass = isInsert
    ? 'text-emerald-900 dark:text-emerald-100'
    : isDelete
    ? 'text-red-900 dark:text-red-200'
    : 'text-gray-700 dark:text-gray-300';

  const prefix = isInsert ? '+' : isDelete ? '-' : ' ';

  return (
    <div className={`flex items-stretch border-b border-gray-100 dark:border-gray-800/60 last:border-0 ${rowClass}`}>
      <div
        className={`w-12 shrink-0 flex items-center justify-center text-xs font-mono py-1.5 border-r ${gutterClass} text-gray-400 dark:text-gray-500`}
      >
        {line.line_number_before ?? ''}
      </div>
      <div
        className={`w-12 shrink-0 flex items-center justify-center text-xs font-mono py-1.5 border-r ${gutterClass} text-gray-400 dark:text-gray-500`}
      >
        {line.line_number_after ?? ''}
      </div>
      <div className="flex-1 flex items-center gap-2 px-3 py-1.5 min-w-0 overflow-x-auto">
        <span className={`shrink-0 w-3 text-xs font-mono select-none ${prefixClass}`}>{prefix}</span>
        <span className={`text-sm font-mono whitespace-pre ${contentClass}`}>{line.content}</span>
      </div>
    </div>
  );
}
