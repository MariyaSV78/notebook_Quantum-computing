import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization.bloch import Bloch

import ipywidgets as widgets
from IPython.display import display


def qiskit_state(theta):
    qc = QuantumCircuit(1)
    qc.ry(2 * theta, 0)
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
    a = np.cos(theta)   # |01>_logical
    b = np.sin(theta)   # |10>_logical
    return bloch_vector(a, b)

def energy_logical(theta, c0, c1, c2, c3, c4, c5, E_nn=0.0):
    return (
        (c0 - c3)
        + (c1 - c2) * np.cos(2 * theta)
        + (c4 + c5) * np.sin(2 * theta)
        + E_nn
    )

def show_bloch_energy(
    energy_vals,
    theta_vals,
    bloch_func,
    figure_description="Bloch sphere",
    interval=250,
    figsize=(9, 4),
    bloch_font_size=10,
    title_pad=20,
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
    ax0 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1 = fig.add_subplot(1, 2, 2)
    plt.subplots_adjust(bottom=0.15, wspace=0.3)

    ax1.plot(theta_vals, energy_vals)
    point, = ax1.plot([], [], "ro", markersize=8)
    vline = ax1.axvline(theta_vals[0], linestyle="--", alpha=0.6)

    ax1.set_xlabel(r"$\theta$")
    ax1.set_ylabel(r"$E(\theta)$")
    ax1.grid(True)

    def update_frame(i):
        theta = theta_vals[i]
        # _, state = qiskit_state(theta)
        vec = bloch_func(theta)
        E = energy_vals[i]

        ax0.cla()
        bloch = Bloch(axes=ax0)
        bloch.font_size = bloch_font_size
        bloch.zlabel = list(z_labels)
        bloch.add_vectors(vec)
        bloch.render()
        ax0.set_title(fr"{figure_description}, $\theta = {theta:.3f}$", pad=title_pad)

        point.set_data([theta], [E])
        vline.set_xdata([theta, theta])
        ax1.set_title(fr"Energy curve, $E(\theta) = {E:.6f}$")

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
    E_min = np.min(energy_vals)
    idx_min = np.argmin(energy_vals)
    theta_min = theta_vals[idx_min]

    widgets.jslink((play, "value"), (slider, "value"))

    def on_value_change(change):
        update_frame(change["new"])

    slider.observe(on_value_change, names="value")

    update_frame(0)

    display(widgets.HBox([play, slider]))
    plt.show()

    return fig, play, slider