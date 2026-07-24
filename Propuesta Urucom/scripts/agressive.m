%% Rebuild Fig. 4 using an optimized 128-tap FIR DC estimator.
%
% The four oscilloscope channels are first resampled to the 2604-Hz
% controller rate. A dedicated DC-estimation branch is then downsampled
% to 84 Hz and filtered using a 128-tap equiripple FIR low-pass filter.
%
% The FIR passband extends to 4 Hz, the stopband begins at 6 Hz, and the
% nominal cutoff is approximately 5 Hz. Zero-phase filtering is used for
% visualization so the estimated DC curves do not contain group delay.

clear;
close all;
clc;

%% File paths

scriptDir = fileparts(mfilename('fullpath'));
paperDir = fileparts(scriptDir);

inputFile = fullfile( ...
    paperDir, ...
    'Imagenes', ...
    'autocalibracionExampleOscilloscope.csv');

outputFile = ...
    'C:\Github\Tesis\docs\Propuesta Urucom\Imagenes\autocalibration_scope_sum.png';

outputDir = fileparts(outputFile);

if ~isfolder(outputDir)
    mkdir(outputDir);
end

%% General configuration

timeColumns = [4 10 16 22];
valueColumns = timeColumns + 1;

labels = {'PGA', 'BP', 'SUM', 'LP'};

colors = [0.10 0.38 0.68;
          0.12 0.55 0.28;
          0.82 0.36 0.10;
          0.50 0.24 0.68];

controllerFs = 2604;

displayStart = 5;
displayEnd = 20;

%% Read oscilloscope records

raw = readmatrix(inputFile);

timeAll = raw(:, timeColumns(1));
signalsAll = raw(:, valueColumns);

% Remove rows without a valid time value.
validRows = isfinite(timeAll);

timeAll = timeAll(validRows);
signalsAll = signalsAll(validRows, :);

% Remove duplicated time samples.
[timeAll, uniqueRows] = unique(timeAll, 'stable');
signalsAll = signalsAll(uniqueRows, :);

% Replace missing channel values through interpolation.
for channel = 1:size(signalsAll, 2)

    signalsAll(:, channel) = fillmissing( ...
        signalsAll(:, channel), ...
        'linear', ...
        'EndValues', 'nearest');

end

%% Resample the oscilloscope records to the controller rate

controllerStart = ceil(timeAll(1) * controllerFs) / controllerFs;
controllerEnd = floor(timeAll(end) * controllerFs) / controllerFs;

controllerTime = ...
    (controllerStart : 1 / controllerFs : controllerEnd).';

controllerSignals = interp1( ...
    timeAll, ...
    signalsAll, ...
    controllerTime, ...
    'linear', ...
    'extrap');

%% Create the reduced-rate DC-estimation branch

% The FIR is not applied directly at 2604 Hz because 128 taps would not
% provide a sufficiently narrow transition around 5 Hz.
decimationFactor = 31;

dcFs = controllerFs / decimationFactor;     % 84 Hz

% resample() applies anti-alias filtering before reducing the sample rate.
dcSignals = resample( ...
    controllerSignals, ...
    1, ...
    decimationFactor);

dcTime = controllerTime(1) + ...
    (0:size(dcSignals, 1)-1).' / dcFs;

%% Design the optimized 128-tap FIR

numberOfTaps = 128;
firOrder = numberOfTaps - 1;

passbandEdgeHz = 4;
stopbandEdgeHz = 6;

nyquistHz = dcFs / 2;

frequencyBands = ...
    [0, passbandEdgeHz, stopbandEdgeHz, nyquistHz] / nyquistHz;

desiredResponse = [1 1 0 0];

% The stopband error is weighted more heavily to obtain a smoother DC
% estimate and stronger rejection of components above approximately 6 Hz.
passbandWeight = 1;
stopbandWeight = 40;

firCoefficients = firpm( ...
    firOrder, ...
    frequencyBands, ...
    desiredResponse, ...
    [passbandWeight stopbandWeight]);

% Normalize the coefficients so the filter has exactly unity gain at DC.
firCoefficients = ...
    firCoefficients / sum(firCoefficients);

%% Apply the optimized FIR

% filtfilt() removes phase delay and squares the magnitude response.
% This is appropriate for offline visualization and figure generation.
dcEstimate = filtfilt( ...
    firCoefficients, ...
    1, ...
    dcSignals);

%% Interpolate the estimated DC back to the original time base

dcEstimateController = interp1( ...
    dcTime, ...
    dcEstimate, ...
    controllerTime, ...
    'pchip', ...
    'extrap');

filteredAll = interp1( ...
    controllerTime, ...
    dcEstimateController, ...
    timeAll, ...
    'linear', ...
    'extrap');

%% Select the displayed interval

displayRows = ...
    timeAll >= displayStart & ...
    timeAll <= displayEnd;

time = timeAll(displayRows);
signals = signalsAll(displayRows, :);
filtered = filteredAll(displayRows, :);

%% Create the figure

fig = figure( ...
    'Color', 'w', ...
    'Position', [100 100 1120 700]);

ax = axes(fig);

hold(ax, 'on');

% Plot the physical oscilloscope records in light gray.
for channel = 1:size(signals, 2)

    plot( ...
        ax, ...
        time, ...
        signals(:, channel), ...
        '--', ...
        'Color', [0.68 0.68 0.68], ...
        'LineWidth', 0.80, ...
        'HandleVisibility', 'off');

end

% Plot the estimated DC curves.
for channel = 1:size(filtered, 2)

    plot( ...
        ax, ...
        time, ...
        filtered(:, channel), ...
        '-', ...
        'Color', colors(channel, :), ...
        'LineWidth', 1.65, ...
        'DisplayName', labels{channel});

end

%% Add direct channel labels

labelTime = 5.35;
labelIndex = find(time >= labelTime, 1, 'first');

if isempty(labelIndex)
    labelIndex = 1;
end

for channel = 1:size(filtered, 2)

    text( ...
        ax, ...
        labelTime, ...
        filtered(labelIndex, channel), ...
        ['  ' labels{channel}], ...
        'Color', colors(channel, :), ...
        'FontWeight', 'bold', ...
        'FontName', 'Times New Roman', ...
        'FontSize', 9, ...
        'HorizontalAlignment', 'left', ...
        'VerticalAlignment', 'bottom');

end

%% Format the figure

xlim(ax, [displayStart displayEnd]);
ylim(ax, [-1.4 1.75]);

xlabel( ...
    ax, ...
    'Time (s)', ...
    'FontName', 'Times New Roman');

ylabel( ...
    ax, ...
    'Stage output relative to V_{ref} (V)', ...
    'FontName', 'Times New Roman');

grid(ax, 'on');
box(ax, 'on');

set( ...
    ax, ...
    'FontName', 'Times New Roman', ...
    'FontSize', 13, ...
    'LineWidth', 0.8, ...
    'GridAlpha', 0.16, ...
    'MinorGridAlpha', 0.08);

%% Export the figure

exportgraphics( ...
    fig, ...
    outputFile, ...
    'Resolution', 300);

%% Print filter and output information

causalGroupDelay = ...
    (numberOfTaps - 1) / (2 * dcFs);

fprintf('\nOptimized DC estimator:\n');
fprintf('  Design:             Equiripple minimax FIR\n');
fprintf('  Number of taps:     %d\n', numberOfTaps);
fprintf('  Original rate:      %.3f Hz\n', controllerFs);
fprintf('  Processing rate:    %.3f Hz\n', dcFs);
fprintf('  Passband edge:      %.2f Hz\n', passbandEdgeHz);
fprintf('  Stopband edge:      %.2f Hz\n', stopbandEdgeHz);
fprintf('  Coefficient sum:    %.9f\n', sum(firCoefficients));
fprintf('  Causal group delay: %.6f s\n', causalGroupDelay);

fprintf('\nSaved figure:\n%s\n', outputFile);