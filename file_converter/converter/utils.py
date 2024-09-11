import lasio
import obspy
import numpy as np
import matplotlib.pyplot as plt


import lasio
import matplotlib.pyplot as plt

def convert_las_to_jpg(las_file, output_jpg):
    las = lasio.read(las_file)
    
    # Get all available keys (log curves) in the LAS file
    available_keys = list(las.keys())

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
                ax_gr.plot(las['GR'], depth, 'g', label='GR')
                ax_gr.set_xlabel('GR')
                ax_gr.legend(loc='upper left')
            if 'SP' in las.keys():
                ax_sp.plot(las['SP'], depth, 'b', label='SP')
                ax_sp.set_xlabel('SP')
                ax_sp.legend(loc='upper right')

        elif log_type == 'MSFL_LLS_LLD':
            ax_msfl_lls_lld = axes[i]
            
            if 'MSFL' in las.keys():
                ax_msfl_lls_lld.plot(las['MSFL'], depth, label='MSFL')
            if 'LLS' in las.keys():
                ax_msfl_lls_lld.plot(las['LLS'], depth, label='LLS')
            if 'LLD' in las.keys():
                ax_msfl_lls_lld.semilogx(las['LLD'], depth, label='LLD')
            
            ax_msfl_lls_lld.set_xlabel('MSFL, LLS, LLD')
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
            
            ax_ral.set_xlabel('RAL1, RAL2, RAL3, RAL4, RAL5')
            ax_ral.legend()

        elif log_type == 'NPHI_RHOB':
            ax_nphi = axes[i]
            ax_rhob = ax_nphi.twiny()
            
            if 'NPHI' in las.keys():
                ax_nphi.plot(las['NPHI'], depth, 'r', label='NPHI')
                ax_nphi.set_xlabel('NPHI')
                ax_nphi.legend(loc='upper left')
                ax_nphi.set_xlim(max(las['NPHI']), min(las['NPHI']))  # Invert NPHI scale
            
            if 'RHOB' in las.keys():
                ax_rhob.plot(las['RHOB'], depth, 'm', label='RHOB')
                ax_rhob.set_xlabel('RHOB')
                ax_rhob.legend(loc='upper right')

        elif log_type == 'DT':
            ax_dt = axes[i]
            
            if 'DT' in las.keys():
                ax_dt.plot(las['DT'], depth, 'm', label='DT')
                ax_dt.set_xlabel('DT')
                ax_dt.legend()
                ax_dt.set_xlim(max(las['DT']), min(las['DT']))  # Invert DT scale

    # Set the y-axis label for depth
    axes[0].set_ylabel('Depth (m)')

    # Invert y-axis for all subplots
    for ax in axes:
        ax.set_ylim(depth.max(), depth.min())

    # Add "Triple Combo" text below the plot
    plt.figtext(0.5, 0.01, "Triple Combo", ha="center", fontsize=12, fontweight='bold')

    # Add the available keys (log curves) below the plot
    available_keys_str = ', '.join(available_keys)  # Join all the available keys into a single string
    plt.figtext(0.5, -0.05, f"This is a preview of the LAS file with some basic logs. Actual LAS files contain a wider range of logs.", ha="center", fontsize=10)
    plt.figtext(0.5, -0.07, f"Available Logs: {available_keys_str}", ha="center", fontsize=10)

    # Adjust layout and save the plot as a JPEG
    plt.tight_layout(rect=[0, 0.06, 1, 1])  # Adjust the rect to make space for the text
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
    plt.savefig(output_jpg, format='jpg', dpi=300, bbox_inches='tight')
    plt.close()
