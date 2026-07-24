% Rebuild the analog-path figure as a wide two-panel layout
% (magnitude | local coherence) for the paper, reusing the computed data in
% the saved .fig. The phase panel is dropped because the paper body only
% analyzes magnitude and coherence.
scriptDir = fileparts(mfilename('fullpath'));
paperDir = fileparts(scriptDir);
inputFile = fullfile(paperDir, 'normalized_geophone_geo_adc_response.fig');
outputFile = fullfile(paperDir, 'Imagenes', 'analog_path_check_sidebyside.png');

fig = openfig(inputFile, 'invisible');
set(fig, 'Color', 'w');

tl = findall(fig, 'Type', 'tiledlayout');
axesAll = findall(fig, 'Type', 'Axes');
axMag = []; axPhase = []; axCoh = [];
for a = axesAll(:)'
    yl = string(a.YLabel.String);
    if any(contains(yl, 'acceleration')), axMag = a; end
    if any(contains(yl, 'Phase')),        axPhase = a; end
    if any(contains(yl, 'coherence')) || any(contains(yl, 'Local')), axCoh = a; end
end

% Drop the phase panel.
if ~isempty(axPhase), delete(axPhase); end

% Reparent the surviving axes (and any legends) out of the tiled layout,
% then remove the layout and place the panels side by side manually.
legendsAll = findall(fig, 'Type', 'Legend');
axMag.Parent = fig;
axCoh.Parent = fig;
for L = legendsAll(:)'
    try
        L.Parent = fig;      % keep legends whose axes survived (magnitude)
    catch
        delete(L);           % drop the orphaned phase-panel legend
    end
end
if ~isempty(tl), delete(tl); end

axMag.Units = 'normalized';
axCoh.Units = 'normalized';
axMag.Position = [0.055 0.170 0.415 0.760];
axCoh.Position = [0.560 0.170 0.405 0.760];

% Both panels now carry a frequency axis.
axMag.XLabel.String = 'Frequency (Hz)';
axCoh.XLabel.String = 'Frequency (Hz)';

% Match the paper's legend wording.
legends = findall(fig, 'Type', 'Legend');
for k = 1:numel(legends)
    entries = string(legends(k).String);
    entries(contains(entries, 'Measured response using the configuration employed in this work')) = ...
        'Measured PGA-output-to-ADC-input path cascaded with nominal SM-24';
    entries(contains(entries, 'Achievable calibration range')) = ...
        'Circuit-tuning envelope (0--2 k$\Omega$ potentiometer sweep)';
    legends(k).String = cellstr(entries);
    legends(k).Interpreter = 'latex';
    legends(k).NumColumns = 1;
    legends(k).FontSize = 10;
end

% Rounded 1 kHz coherence-onset marker on both log-x panels.
panels = {axMag, axCoh};
for pIdx = 1:numel(panels)
    a = panels{pIdx};
    if isgraphics(a) && strcmpi(a.XScale, 'log')
        xline(a, 1e3, '-.', 'Color', [0.35 0.35 0.35], ...
            'LineWidth', 1.2, 'HandleVisibility', 'off');
        a.FontSize = 12;
    end
end

% Wide, short canvas for a full-width, low-height paper float.
set(fig, 'Position', [100 100 1750 620]);
drawnow;
exportgraphics(fig, outputFile, 'Resolution', 300, 'BackgroundColor', 'white');
close(fig);
fprintf('Saved side-by-side figure: %s\n', outputFile);
