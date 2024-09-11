import lasio
import obspy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.image as image
from PIL import Image as PILImage
import re

def convert_las_to_jpg(las_file, output_jpg):
    las = lasio.read(las_file)
    
    # Get all available keys (log curves) and their units
    available_keys = [(curve.mnemonic, curve.unit) for curve in las.curves]

    # Define the available logs and the corresponding axis titles
    available_logs = []
    
    if 'GR' in las.keys() or 'SP' in las.keys():
        available_logs.append('GR_SP')
    if 'MSFL' in las.keys() or 'LLS' in las.keys() or 'LLD' in las.keys():
        available_logs.append('MSFL_LLS_LLD')
    if 'RAL1' in las.keys() or 'RAL2' in las.keys() or 'RAL3' in las.keys() or 'RAL4' in las.keys() or 'RAL5' in las.keys():
        available_logs.append('RAL')
    if 'NPHI' in las.keys() or 'RHOB' in las.keys():
        available_logs.append('NPHI_RHOB')
    if 'DT' in las.keys():
        available_logs.append('DT')

    # If no logs are available, print a message and return
    if not available_logs:
        print("No logs available for plotting.")
        return

    # Dynamically set figure width based on the number of available logs
    plot_width_per_log = 4.5  # Width per subplot
    fig_width = len(available_logs) * plot_width_per_log
    fig, axes = plt.subplots(ncols=len(available_logs), figsize=(fig_width, 10))  # Height fixed at 10 units

    # Ensure that axes is always iterable
    if len(available_logs) == 1:
        axes = [axes]

    # Get depth values
    depth = las['DEPT']
    
    # Iterate through the available logs and plot them
    for i, log_type in enumerate(available_logs):
        if log_type == 'GR_SP':
            ax_gr = axes[i]
            ax_sp = ax_gr.twiny()
            
            if 'GR' in las.keys():
                unit_gr = next((curve.unit for curve in las.curves if curve.mnemonic == 'GR'), '')
                xlabel_gr = f'GR ({unit_gr})' if unit_gr else 'GR'
                ax_gr.plot(las['GR'], depth, 'g', label='GR')
                ax_gr.set_xlabel(xlabel_gr)
                ax_gr.legend(loc='upper left')
            if 'SP' in las.keys():
                unit_sp = next((curve.unit for curve in las.curves if curve.mnemonic == 'SP'), '')
                xlabel_sp = f'SP ({unit_sp})' if unit_sp else 'SP'
                ax_sp.plot(las['SP'], depth, 'b', label='SP')
                ax_sp.set_xlabel(xlabel_sp)
                ax_sp.legend(loc='upper right')

        elif log_type == 'MSFL_LLS_LLD':
            ax_msfl_lls_lld = axes[i]
            
            if 'MSFL' in las.keys():
                ax_msfl_lls_lld.plot(las['MSFL'], depth, label='MSFL')
            if 'LLS' in las.keys():
                ax_msfl_lls_lld.plot(las['LLS'], depth, label='LLS')
            if 'LLD' in las.keys():
                ax_msfl_lls_lld.semilogx(las['LLD'], depth, label='LLD')
            
            xlabel = ', '.join([f'{log} ({unit})' if unit else log for log, unit in [('MSFL', next((curve.unit for curve in las.curves if curve.mnemonic == 'MSFL'), '')),
                                                                                     ('LLS', next((curve.unit for curve in las.curves if curve.mnemonic == 'LLS'), '')),
                                                                                     ('LLD', next((curve.unit for curve in las.curves if curve.mnemonic == 'LLD'), ''))] if log in las.keys()])
            ax_msfl_lls_lld.set_xlabel(xlabel)
            ax_msfl_lls_lld.legend()
        
        elif log_type == 'RAL':
            ax_ral = axes[i]
            
            if 'RAL1' in las.keys():
                ax_ral.plot(las['RAL1'], depth, label='RAL1')
            if 'RAL2' in las.keys():
                ax_ral.plot(las['RAL2'], depth, label='RAL2')
            if 'RAL3' in las.keys():
                ax_ral.plot(las['RAL3'], depth, label='RAL3')
            if 'RAL4' in las.keys():
                ax_ral.plot(las['RAL4'], depth, label='RAL4')
            if 'RAL5' in las.keys():
                ax_ral.plot(las['RAL5'], depth, label='RAL5')

            xlabel = ', '.join([f'{log} ({unit})' if unit else log for log, unit in [('RAL1', next((curve.unit for curve in las.curves if curve.mnemonic == 'RAL1'), '')),
                                                                                     ('RAL2', next((curve.unit for curve in las.curves if curve.mnemonic == 'RAL2'), '')),
                                                                                     ('RAL3', next((curve.unit for curve in las.curves if curve.mnemonic == 'RAL3'), '')),
                                                                                     ('RAL3', next((curve.unit for curve in las.curves if curve.mnemonic == 'RAL4'), '')),
                                                                                     ('RAL3', next((curve.unit for curve in las.curves if curve.mnemonic == 'RAL5'), '')),] if log in las.keys()])
            ax_ral.set_xlabel(xlabel)
            ax_ral.legend()

        elif log_type == 'NPHI_RHOB':
            ax_nphi = axes[i]
            ax_rhob = ax_nphi.twiny()
            
            if 'NPHI' in las.keys():
                unit_nphi = next((curve.unit for curve in las.curves if curve.mnemonic == 'NPHI'), '')
                xlabel_nphi = f'NPHI ({unit_nphi})' if unit_nphi else 'NPHI'
                ax_nphi.plot(las['NPHI'], depth, 'r', label='NPHI')
                ax_nphi.set_xlabel(xlabel_nphi)
                ax_nphi.legend(loc='upper left')
                ax_nphi.set_xlim(max(las['NPHI']), min(las['NPHI']))  # Invert NPHI scale
            
            if 'RHOB' in las.keys():
                unit_rhob = next((curve.unit for curve in las.curves if curve.mnemonic == 'RHOB'), '')
                xlabel_rhob = f'RHOB ({unit_rhob})' if unit_rhob else 'RHOB'
                ax_rhob.plot(las['RHOB'], depth, 'm', label='RHOB')
                ax_rhob.set_xlabel(xlabel_rhob)
                ax_rhob.legend(loc='upper right')

        elif log_type == 'DT':
            ax_dt = axes[i]
            
            if 'DT' in las.keys():
                unit_dt = next((curve.unit for curve in las.curves if curve.mnemonic == 'DT'), '')
                xlabel_dt = f'DT ({unit_dt})' if unit_dt else 'DT'
                ax_dt.plot(las['DT'], depth, 'm', label='DT')
                ax_dt.set_xlabel(xlabel_dt)
                ax_dt.legend()
                ax_dt.set_xlim(max(las['DT']), min(las['DT']))  # Invert DT scale

    # Set the y-axis label for depth
    axes[0].set_ylabel('Depth (m)')

    # Invert y-axis for all subplots
    for ax in axes:
        ax.set_ylim(depth.max(), depth.min())

    log_name = las.well["WELL"].value if "WELL" in las.well else "Unknown Log"
    plt.suptitle(f"Bapex - {log_name}", fontsize=12, fontweight='bold', ha='center')

    plt.figtext(0.5, 0.01, "Triple Combo", ha="center", fontsize=14, fontweight='bold')

    # Prepare available keys and units string
    plt.figtext(0.5, -0.05, f"This is a preview of the LAS file with some basic logs. Actual LAS files contain a wider range of logs.", ha="center", fontsize=10)
    available_keys_with_units = ', '.join([f"{key}" if unit else key for key, unit in available_keys])
    # Add the available keys (log curves with units) below the plot
    plt.figtext(0.5, -0.07, f"Available Curves: {available_keys_with_units}", ha="center", fontsize=10)


    with cbook.get_sample_data('BAPEX.png') as file:
        pil_image = PILImage.open(file)
        # Resize image: Change the size as needed
        new_size = (400, 200)  # Width x Height
        pil_image = pil_image.resize(new_size, PILImage.ANTIALIAS)
        im = np.array(pil_image)
    # Calculate watermark position (center of the figure)
    fig_width, fig_height = fig.get_size_inches() * fig.get_dpi()
    im_width, im_height = im.shape[1], im.shape[0]
    x = (fig_width - im_width) / 2
    y = (fig_height - im_height) / 2

    # Add the watermark image
    fig.figimage(im, x, y, zorder=3, alpha=0.5)

    plt.savefig(output_jpg, format='jpeg', bbox_inches='tight')
    plt.close(fig)

def convert_sgy_to_jpg(sgy_file, output_jpg, sampling_interval=0.004):
    stream = obspy.read(sgy_file)
    data = np.stack([tr.data for tr in stream])
    norm_data = np.apply_along_axis(lambda x: x / np.max(np.abs(x)), 1, data)
    time_axis = np.arange(norm_data.shape[1]) * sampling_interval
    fig, ax = plt.subplots(figsize=(20, 8))
    ax.imshow(norm_data.T, aspect='auto', cmap='seismic', vmin=-1, vmax=1,
              extent=[0, norm_data.shape[0], time_axis[-1], time_axis[0]])
    ax.set_title(f'SEG-Y Data: {sgy_file}')
    ax.set_xlabel('Trace Number')
    ax.set_ylabel('Time (s)')

    lines = stream.stats.textual_file_header.decode('ascii').split('\n')
    company = re.search(r'COMPANY\s+(\w+)', lines[0])
    line_info = re.search(r'LINE\s+:\s+(\S+)', lines[0])
    area = re.search(r'AREA\s+:\s+(\S+)', lines[0])

    # Format extracted information
    company = company.group(1) if company else "Unknown"
    line_info = line_info.group(1) if line_info else "Unknown"
    area = area.group(1) if area else "Unknown"

    plt.suptitle(f"{company} - {area} - {line_info}", fontsize=12, fontweight='bold', ha='center')

    with cbook.get_sample_data('BAPEX.png') as file:
        pil_image = PILImage.open(file)
        # Resize image: Change the size as needed
        new_size = (1500, 900)  # Width x Height
        pil_image = pil_image.resize(new_size, PILImage.ANTIALIAS)
        im = np.array(pil_image)
    # Calculate watermark position (center of the figure)
    fig_width, fig_height = fig.get_size_inches() * fig.get_dpi()
    im_width, im_height = im.shape[1], im.shape[0]
    x = (fig_width - im_width) / 2
    y = (fig_height - im_height) / 2

    fig.figimage(im, 1500, 500, zorder=3, alpha=0.3)

    plt.savefig(output_jpg, format='jpg', dpi=300, bbox_inches='tight')
    plt.close()
