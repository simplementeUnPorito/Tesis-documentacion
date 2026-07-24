%% Wide wiggle-trace waterfall for the field record (paper Fig. 5).
% Reads waterfall.csv (22 column pairs: 21 geophone traces at 10-50 m plus a
% hammer trace near 8 m). Each trace is drawn with variable-area (black)
% fill of its positive lobes, on a wide, short canvas so the figure fits as
% a full-width, low-height float.

clear; close all; clc;

scriptDir = fileparts(mfilename('fullpath'));
paperDir  = fileparts(scriptDir);
csvFile   = fullfile(scriptDir, 'waterfall.csv');
outFile   = fullfile(paperDir, 'Imagenes', 'waterfall_wiggle_horizontal.png');

raw = readmatrix(csvFile);            % skips the header row automatically
nTraces = size(raw, 2) / 2;

fig = figure('Color', 'w', 'Position', [100 100 1040 760]);
set(fig, 'DefaultAxesToolbarVisible', 'off');
ax = axes(fig); hold(ax, 'on');

hammerColor = [0.10 0.30 0.55];

for k = 1:nTraces
    t = raw(:, 2*k-1) * 1000;         % s -> ms
    y = raw(:, 2*k);
    good = isfinite(t) & isfinite(y);
    t = t(good); y = y(good);
    base = median(y(max(1,end-400):end));

    isHammer = base < 9.5;

    if isHammer
        plot(ax, t, -1*y+2*mean(y), '-', 'Color', hammerColor, 'LineWidth', 1.4);
        text(ax, 250, base, '  Hammer', 'Color', hammerColor, ...
            'FontWeight', 'bold', 'FontName', 'Times New Roman', ...
            'FontSize', 12, 'VerticalAlignment', 'bottom');
    else
        yFill = max(y, base);
        fill(ax, [t(1); t; t(end)], [base; yFill; base], [0 0 0], ...
            'EdgeColor', 'none');
        plot(ax, t, y, '-', 'Color', [0 0 0], 'LineWidth', 0.6);
    end
end

xline(ax, 0, '--', 'Color', [0.45 0.45 0.45], 'LineWidth', 1.0, ...
    'HandleVisibility', 'off');


xlim(ax, [-50 2500]);
ylim(ax, [6.5 51.5]);
yticks(ax, 10:4:50);
xlabel(ax, 'Time after impact (ms)', 'FontName', 'Times New Roman');
ylabel(ax, 'Source-receiver distance (m)', 'FontName', 'Times New Roman');
grid(ax, 'on'); box(ax, 'on');
set(ax, 'FontName', 'Times New Roman', 'FontSize', 13, ...
    'LineWidth', 0.9, 'GridAlpha', 0.14, 'Layer', 'top');

exportgraphics(fig, outFile, 'Resolution', 300);
fprintf('Saved wide waterfall: %s\n', outFile);
