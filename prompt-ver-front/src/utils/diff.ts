import type { DiffLineResponse, VersionDiffResponse } from '../types';

function buildLCS(a: string[], b: string[]): number[][] {
  const m = a.length;
  const n = b.length;
  const dp: number[][] = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1] ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1]);
    }
  }
  return dp;
}

function backtrack(dp: number[][], a: string[], b: string[], i: number, j: number): DiffLineResponse[] {
  if (i === 0 && j === 0) return [];
  if (i === 0) {
    return [
      ...backtrack(dp, a, b, i, j - 1),
      { kind: 'insert', content: b[j - 1], line_number_before: null, line_number_after: j },
    ];
  }
  if (j === 0) {
    return [
      ...backtrack(dp, a, b, i - 1, j),
      { kind: 'delete', content: a[i - 1], line_number_before: i, line_number_after: null },
    ];
  }
  if (a[i - 1] === b[j - 1]) {
    return [
      ...backtrack(dp, a, b, i - 1, j - 1),
      { kind: 'equal', content: a[i - 1], line_number_before: i, line_number_after: j },
    ];
  }
  if (dp[i - 1][j] >= dp[i][j - 1]) {
    return [
      ...backtrack(dp, a, b, i - 1, j),
      { kind: 'delete', content: a[i - 1], line_number_before: i, line_number_after: null },
    ];
  }
  return [
    ...backtrack(dp, a, b, i, j - 1),
    { kind: 'insert', content: b[j - 1], line_number_before: null, line_number_after: j },
  ];
}

export function computeDiff(
  promptId: string,
  versionIdBefore: string,
  versionIdAfter: string,
  versionNumberBefore: number,
  versionNumberAfter: number,
  contentBefore: string,
  contentAfter: string
): VersionDiffResponse {
  const aLines = contentBefore.split('\n');
  const bLines = contentAfter.split('\n');
  const dp = buildLCS(aLines, bLines);
  const lines = backtrack(dp, aLines, bLines, aLines.length, bLines.length);
  const hasChanges = lines.some((l) => l.kind !== 'equal');

  return {
    prompt_id: promptId,
    version_id_before: versionIdBefore,
    version_id_after: versionIdAfter,
    version_number_before: versionNumberBefore,
    version_number_after: versionNumberAfter,
    lines,
    has_changes: hasChanges,
  };
}
