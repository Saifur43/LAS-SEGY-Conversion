import lasio
import obspy
import numpy as np
import matplotlib.pyplot as plt

# Function to convert LAS file to JPG
def convert_las_to_jpg(las_file, output_jpg):
    las = lasio.read(las_file)
    fig, axes = plt.subplots(ncols=4, figsize=(18, 10))
    depth = las['DEPT']

    ax_gr = axes[0]
    ax_sp = ax_gr.twiny()

    if 'GR' in las.keys():
        ax_gr.plot(las['GR'], depth, 'g', label='GR')
        ax_gr.set_xlabel('GR')
        ax_gr.legend(loc='upper left')
    if 'SP' in las.keys():
        ax_sp.plot(las['SP'], depth, 'b', label='SP')
        ax_sp.set_xlabel('SP')
        ax_sp.legend(loc='upper right')

    ax_msfl_lls_lld = axes[1]
    if 'MSFL' in las.keys():
        ax_msfl_lls_lld.plot(las['MSFL'], depth, label='MSFL')
    if 'LLS' in las.keys():
        ax_msfl_lls_lld.plot(las['LLS'], depth, label='LLS')
    if 'LLD' in las.keys():
        ax_msfl_lls_lld.semilogx(las['LLD'], depth, label='LLD')
    ax_msfl_lls_lld.set_xlabel('MSFL, LLS, LLD')
    ax_msfl_lls_lld.legend()

    ax_nphi = axes[2]
    ax_rhob = ax_nphi.twiny()
    if 'NPHI' in las.keys():
        ax_nphi.plot(las['NPHI'], depth, 'r', label='NPHI')
        ax_nphi.set_xlabel('NPHI')
        ax_nphi.legend(loc='upper left')
        ax_nphi.set_xlim(max(las['NPHI']), min(las['NPHI']))

    if 'RHOB' in las.keys():
        ax_rhob.plot(las['RHOB'], depth, 'm', label='RHOB')
        ax_rhob.set_xlabel('RHOB')
        ax_rhob.legend(loc='upper right')

    ax_dt = axes[3]
    if 'DT' in las.keys():
        ax_dt.plot(las['DT'], depth, 'm', label='DT')
        ax_dt.set_xlabel('DT')
        ax_dt.legend()
        ax_dt.set_xlim(max(las['DT']), min(las['DT']))

    axes[0].set_ylabel('Depth (m)')
    for ax in axes:
        ax.set_ylim(depth.max(), depth.min())

    plt.figtext(0.5, 0.01, "Triple Combo", ha="center", fontsize=12, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 1])
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
