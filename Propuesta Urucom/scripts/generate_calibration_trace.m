%% Rebuild Fig. 4 from the four-channel Tektronix export.
% The oscilloscope records are resampled to the 2604-Hz controller rate and
% processed with the exact 128-tap Q1.23 coefficient vector in the PSoC
% firmware. The filtered curves are then interpolated to the scope time base.

clear;
close all;

scriptDir = fileparts(mfilename('fullpath'));
paperDir = fileparts(scriptDir);
inputFile = fullfile(paperDir, 'Imagenes', ...
    'autocalibracionExampleOscilloscope.csv');
outputFile = fullfile(paperDir, 'Imagenes', ...
    'autocalibration_scope_sum.png');
coefficientFile = fullfile(paperDir, '..', '..', 'firmware', 'psoc', ...
    'AcondicionamientoAnalogico.cydsn', 'FIR_calibration.h');

raw = readmatrix(inputFile);
timeColumns = [4 10 16 22];
valueColumns = timeColumns + 1;
labels = {'PGA', 'BP', 'SUM', 'LP'};
colors = [0.10 0.38 0.68; 0.12 0.55 0.28; ...
          0.82 0.36 0.10; 0.50 0.24 0.68];

timeAll = raw(:, timeColumns(1));
signalsAll = raw(:, valueColumns);
validRows = isfinite(timeAll);
timeAll = timeAll(validRows);
signalsAll = signalsAll(validRows, :);
[timeAll, uniqueRows] = unique(timeAll, 'stable');
signalsAll = signalsAll(uniqueRows, :);
for channel = 1:size(signalsAll, 2)
    signalsAll(:, channel) = fillmissing(signalsAll(:, channel), ...
        'linear', 'EndValues', 'nearest');
end

% Decode the firmware's little-endian Q1.23 coefficient bytes.
coefficientText = fileread(coefficientFile);
tokens = regexp(coefficientText, '0x([0-9A-Fa-f]{2})u', 'tokens');
coefficientBytes = uint8(cellfun(@(token) hex2dec(token{1}), tokens));
assert(numel(coefficientBytes) == 4 * 128, ...
    'Expected 128 four-byte FIR coefficients in FIR_calibration.h.');
byteMatrix = reshape(double(coefficientBytes), 4, []).';
coefficientWords = byteMatrix(:, 1) + 2^8 * byteMatrix(:, 2) + ...
    2^16 * byteMatrix(:, 3) + 2^24 * byteMatrix(:, 4);
coefficientWords(coefficientWords >= 2^31) = ...
    coefficientWords(coefficientWords >= 2^31) - 2^32;
firCoefficients = coefficientWords / 2^23;

controllerFs = 2604;
controllerTime = (ceil(timeAll(1) * controllerFs) / controllerFs : ...
    1 / controllerFs : floor(timeAll(end) * controllerFs) / controllerFs).';
controllerSignals = interp1(timeAll, signalsAll, controllerTime, ...
    'linear', 'extrap');
controllerFiltered = filter(firCoefficients, 1, controllerSignals);
filteredAll = interp1(controllerTime, controllerFiltered, timeAll, ...
    'linear', 'extrap');

displayRows = timeAll >= 5 & timeAll <= 20;
time = timeAll(displayRows);
signals = signalsAll(displayRows, :);
filtered = filteredAll(displayRows, :);

fig = figure('Color', 'w', 'Position', [100 100 1020 650]);
ax = axes(fig);
hold(ax, 'on');

% Draw the physical records first in light gray so the filtered colored
% curves remain visually dominant.
for channel = 1:size(signals, 2)
    plot(ax, time, signals(:, channel), '--', ...
        'Color', [0.64 0.64 0.64], 'LineWidth', 0.85, ...
        'HandleVisibility', 'off');
end
for channel = 1:size(filtered, 2)
    plot(ax, time, filtered(:, channel), '-', ...
        'Color', colors(channel, :), 'LineWidth', 1.55, ...
        'DisplayName', labels{channel});
end

labelTime = 5.35;
labelIndex = find(time >= labelTime, 1, 'first');
for channel = 1:size(filtered, 2)
    text(ax, labelTime, filtered(labelIndex, channel), labels{channel}, ...
        'Color', colors(channel, :), 'FontWeight', 'bold', ...
        'FontName', 'Times New Roman', 'FontSize', 9, ...
        'HorizontalAlignment', 'left', 'VerticalAlignment', 'bottom');
end

xlim(ax, [5 20]);
ylim(ax, [-1.4 1.75]);
xlabel(ax, 'Time (s)');
ylabel(ax, 'Stage output relative to V_{ref} (V)');
grid(ax, 'on');
box(ax, 'on');
set(ax, 'FontName', 'Times New Roman', 'FontSize', 10, ...
    'LineWidth', 0.8, 'GridAlpha', 0.16, 'MinorGridAlpha', 0.08);

exportgraphics(fig, outputFile, 'Resolution', 300);
fprintf('Updated calibration trace with %d firmware taps (sum %.9f): %s\n', ...
    numel(firCoefficients), sum(firCoefficients), outputFile);
