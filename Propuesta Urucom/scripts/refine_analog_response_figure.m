% Relabel the circuit-response figure for the paper without altering the
% original analysis artifact. The measured quantity is CH4/CH1, the
% monitored-input-to-LP-output path; the geophone factor is nominal.
scriptDir = fileparts(mfilename('fullpath'));
paperDir = fileparts(scriptDir);
inputFile = fullfile(paperDir, 'normalized_geophone_geo_adc_response.fig');
outputFile = fullfile(paperDir, 'Imagenes', 'analog_path_check.png');

fig = openfig(inputFile, 'invisible');

legends = findall(fig, 'Type', 'Legend');
for index = 1:numel(legends)
    entries = string(legends(index).String);
    match = contains(entries, 'Measured response using the configuration employed in this work');
    entries(match) = 'Measured PGA-output-to-ADC-input path cascaded with nominal SM-24';
    tuningMatch = contains(entries, 'Achievable calibration range');
    entries(tuningMatch) = 'Circuit-tuning envelope (0--2 k$\Omega$ potentiometer sweep)';
    legends(index).String = cellstr(entries);
    legends(index).Interpreter = 'latex';
end

% Mark the approximate boundary above which the strongly attenuated sweep
% loses local coherence and the available measurement chain becomes
% unreliable.  The boundary is intentionally rounded to 1 kHz: the first
% measured coherence value below 0.9 occurs at approximately 0.84 kHz.
reliabilityHz = 1e3;
axesObjects = findall(fig, 'Type', 'Axes');
for index = 1:numel(axesObjects)
    axisHandle = axesObjects(index);
    if strcmpi(axisHandle.XScale, 'log')
        marker = xline(axisHandle, reliabilityHz, '-.', ...
            'Color', [0.35 0.35 0.35], 'LineWidth', 1.2, ...
            'HandleVisibility', 'off');
        yLabelText = string(axisHandle.YLabel.String);
        if any(contains(yLabelText, 'Normalized acceleration sensitivity'))
            marker.Label = 'Approx. reliability limit (1 kHz)';
            marker.LabelHorizontalAlignment = 'right';
            marker.LabelVerticalAlignment = 'bottom';
            marker.FontSize = 8;
        end
    end
end

exportgraphics(fig, outputFile, 'Resolution', 300, 'BackgroundColor', 'white');
if isgraphics(fig)
    close(fig);
end
fprintf('Updated analog-path figure: %s\n', outputFile);
