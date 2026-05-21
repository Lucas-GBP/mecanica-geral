from __future__ import annotations
from typing import Callable, Literal
from utils.linear_algebra import Vec3, sum_vec3

type ForceFunc = Callable[["Particle"], Vec3] # Defnição de um tipo para funções de força, que recebem uma partícula e retornam um vetor de força
type SimulationTypes = Literal["Euler", "RK4"] # Definição de um tipo para os tipos de simulação disponíveis, que podem ser "Euler" ou "Runge–Kutta de quarta ordem"

class Particle:
    mass: float
    position: Vec3
    velocity: Vec3
    simulation_type: SimulationTypes

    def __init__(self,
        mass: float,
        position: Vec3,
        velocity: Vec3,
        simulation_type: SimulationTypes = "RK4"
    ) -> None:
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.simulation_type = simulation_type
        return

    def __repr__(self) -> str:
        return f"Particle(mass={self.mass}, position={self.position}, velocity={self.velocity}, simulation_type={self.simulation_type})"

    def update(self, forces: list[ForceFunc], dt: float) -> None:
        if self.simulation_type == "Euler":
            self._euler_update(forces, dt)
            return

        if self.simulation_type == "RK4":
            self._rk4_update(forces, dt)
            return

        raise ValueError(f"Unsupported simulation type: {self.simulation_type}")

    def _euler_update(self, forces: list[ForceFunc], dt: float) -> None:
        acceleration = sum_vec3(force(self) for force in forces) / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        return

    def _compute_expliced_acceleration(
        self,
        forces: list[ForceFunc],
        position: Vec3,
        velocity: Vec3,
    ) -> Vec3:
        state = Particle(
            mass=self.mass,
            position=position,
            velocity=velocity,
            simulation_type=self.simulation_type,
        )
        total_force = sum_vec3(force(state) for force in forces)
        return total_force / self.mass

    def _rk_iteration(
        self,
        forces: list[ForceFunc],
        dt: float,
        dxdt: Vec3,
        dvdt: Vec3,
    ) -> tuple[Vec3, Vec3]:
        # Em cada estágio, RK4 avalia f(x, v) = (v, a(x, v)).
        next_dxdt = self.velocity + dvdt * dt
        next_dvdt = self._compute_expliced_acceleration(
            forces,
            self.position + dxdt * dt,
            self.velocity + dvdt * dt
        )
        return next_dxdt, next_dvdt

    def _rk4_update(self, forces: list[ForceFunc], dt: float) -> None:
        half_dt = dt / 2.0
        vector_zero = Vec3(0, 0, 0)

        # primeira interação
        k1_dxdt, k1_dvdt = self._rk_iteration(
            forces,
            half_dt,
            vector_zero,
            vector_zero,
        )
        # segunda interação
        k2_dxdt, k2_dvdt = self._rk_iteration(
            forces,
            half_dt,
            k1_dxdt,
            k1_dvdt
        )
        # terceira interação
        k3_dxdt, k3_dvdt = self._rk_iteration(
            forces,
            half_dt,
            k2_dxdt,
            k2_dvdt
        )
        # quarta interação
        k4_dxdt, k4_dvdt = self._rk_iteration(
            forces,
            dt,
            k3_dxdt,
            k3_dvdt
        )

        # Combina as quatro avaliações com os pesos clássicos 1-2-2-1.
        self.position += (
            k1_dxdt
            + k2_dxdt * 2.0
            + k3_dxdt * 2.0
            + k4_dxdt
        ) * (dt / 6.0)
        self.velocity += (
            k1_dvdt
            + k2_dvdt * 2.0
            + k3_dvdt * 2.0
            + k4_dvdt
        ) * (dt / 6.0)
        return
