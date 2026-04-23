import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization.bloch import Bloch

import ipywidgets as widgets
from IPython.display import display
import matplotlib.gridspec as gridspec

def qiskit_state(theta):
    qc = QuantumCircuit(1)
    qc.ry(2 * theta, 0)
    state = Statevector.from_instruction(qc)
    return qc, state

def qiskit_state_h2(theta):
    qc = QuantumCircuit(2)
    qc.initialize([0, np.cos(theta), np.sin(theta), 0], [0, 1])
    state = Statevector.from_instruction(qc)
    return qc, state

def bloch_vector(a,b):
    x = 2 * np.real(np.conj(a) * b)
    y = 2 * np.imag(np.conj(b) * a)
    z = np.abs(a) ** 2 - np.abs(b) ** 2
    return [x, y, z]

def bloch_vector_h(theta):
    """
    Bloch vector for the 1-qubit H ansatz:
        |psi(theta)> = cos(theta)|0> + sin(theta)|1>
    """
    _, state = qiskit_state(theta)
    #from state
    a = state.data[0]
    b = state.data[1]
    #from amplitues
    # a = np.cos(theta)
    # b = np.sin(theta)
    return bloch_vector(a, b)


def bloch_vector_h2plus(theta):
    """
    Logical Bloch vector for the H2+ ansatz in the subspace {|10>, |01>}:
        |psi(theta)> = cos(theta)|10> + sin(theta)|01>

    We identify:
        |0_L> = |10>
        |1_L> = |01>
    """
    #from amplitudes
    a = np.cos(theta)   # amplitude of |10>
    b = np.sin(theta)   # amplitude of |01>
    return bloch_vector(a, b)

def bloch_vector_h2(theta):
    # Matches your actual ansatz:
    # |psi(theta)> = cos(theta)|0> - sin(theta)|1>
    a = np.cos(theta)
    b = -np.sin(theta)
    return bloch_vector(a, b)

def qiskit_state_h2_logical(theta):
    qc = QuantumCircuit(1)
    qc.ry(-theta, 0)
    state = Statevector.from_instruction(qc)
    return qc, state

def bloch_vector_h2_logical(theta):
    # _, state = qiskit_state_h2_logical(theta)
    # a = state.data[0]
    # b = state.data[1]

    a = np.cos(theta)
    b = -np.sin(theta)
    return bloch_vector(a, b)


def show_bloch_energy(
    energy_vals,
    theta_vals,
    bloch_func,
    figure_description="Bloch sphere",
    interval=250,
    figsize=(10, 4),
    bloch_font_size=10,
    title_pad=40,
    slider_description="Frame",
    z_labels=(r"$|0\rangle$", r"$|1\rangle$")
):
    """
    This function creates a dynamic interface combining:
    - a Bloch sphere showing the quantum state |ψ(θ)>
    - an energy curve E(θ)
  
    Returns
    -------
        - 'fig' : matplotlib Figure
        - 'play' : ipywidgets Play widget
        - 'slider' : ipywidgets IntSlider

    Notes
    -----
    - Requires a Jupyter environment with `%matplotlib widget`.
    - Designed for visualizing VQE-like parameter sweeps.
    """   

    plt.close("all")

    fig = plt.figure(figsize=figsize)

    gs = gridspec.GridSpec(
    1, 2,
    width_ratios=[1, 1.3],  # ← make second plot larger
    wspace=0.4            # ← control spacing here
    )

    ax0 = fig.add_subplot(gs[0], projection="3d")
    ax1 = fig.add_subplot(gs[1])
    plt.subplots_adjust(bottom=0.15, wspace=1)

    ax1.plot(theta_vals, energy_vals)
    point, = ax1.plot([], [], "ro", markersize=8)
    vline = ax1.axvline(theta_vals[0], linestyle="--", alpha=0.6)

    ax1.set_xlabel(r"$\theta$")
    ax1.set_ylabel(r"$E(\theta)$")
    ax1.grid(True)

    def update_frame(i):
        theta = theta_vals[i]
        # _, state = qiskit_state(theta)
        # vec = bloch_func(theta)
        E = energy_vals[i]

        if i == len(theta_vals) - 1:
            idx_min = np.argmin(energy_vals)
            theta = theta_vals[idx_min]
            E = energy_vals[idx_min]
        
        vec = bloch_func(theta)
  
        ax0.cla()
        bloch = Bloch(axes=ax0)
        bloch.font_size = bloch_font_size
        bloch.zlabel = list(z_labels)
        bloch.add_vectors(vec)
        bloch.render()
        # ax0.set_title(fr"{figure_description} \n$\theta = {theta:.3f}$", pad=title_pad)
        ax0.set_title(figure_description, pad=title_pad)

        ax0.text2D(
            0.5, 1.03,   # move higher
            fr"$\theta = {theta:.3f}$",
            transform=ax0.transAxes,
            ha="center"
        )

        point.set_data([theta], [E])
        vline.set_xdata([theta, theta])
        ax1.set_title(fr"Energy curve, $E(\theta) = {E:.6f}$", pad=15)
        if i == len(theta_vals) - 1:
            idx_min = np.argmin(energy_vals)
            theta_min = theta_vals[idx_min]
            E_min = energy_vals[idx_min]

            point.set_data([theta_min], [E_min])
            vline.set_xdata([theta_min, theta_min]) 
            
            ax1.set_title(fr"Energy curve, $E(\theta) = {E_min:.6f}$", pad=15)

        fig.canvas.draw_idle()


    play = widgets.Play(
        value=0,
        min=0,
        max=len(theta_vals) - 1,
        step=1,
        interval=interval,
        description="Press play",
        disabled=False,
    )

    slider = widgets.IntSlider(
        value=0,
        min=0,
        max=len(theta_vals) - 1,
        step=1,
        description=slider_description,
        continuous_update=False,
    )

    widgets.jslink((play, "value"), (slider, "value"))

    def on_value_change(change):
        update_frame(change["new"])

    slider.observe(on_value_change, names="value")

    update_frame(0)

    display(widgets.HBox([play, slider]))
    plt.show()

    return fig, play, slider