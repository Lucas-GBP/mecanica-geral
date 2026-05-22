from __future__ import annotations
from typing import Callable, Literal
from utils.linear_algebra import Vec3, sum_vec3

type ForceFunc = Callable[["Particle", float|None], Vec3] # Defnição de um tipo para funções de força, que recebem uma partícula e retornam um vetor de força
type UpdateFunc = Callable[[list[ForceFunc], float, float|None], None] # Definição de um tipo para funções de atualização, que recebem uma lista de funções de força, o tempo atual e um intervalo de tempo, e não retornam nada
type SimulationTypes = Literal["Euler", "RK4"] # Definição de um tipo para os tipos de simulação disponíveis, que podem ser "Euler" ou "Runge–Kutta de quarta ordem"

class Particle:
    mass: float
    position: Vec3
    velocity: Vec3
    _simulation_type: SimulationTypes
    _update_impl: UpdateFunc

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

    @property
    def simulation_type(self) -> SimulationTypes:
        return self._simulation_type

    @simulation_type.setter
    def simulation_type(self, simulation_type: SimulationTypes) -> None:
        self._simulation_type = simulation_type
        self._update_impl = self._resolve_update_impl(simulation_type)

    def _resolve_update_impl(
        self,
        simulation_type: SimulationTypes,
    ) -> UpdateFunc:
        if simulation_type == "Euler":
            return self._euler_update

        if simulation_type == "RK4":
            return self._rk4_update

        raise ValueError(f"Unsupported simulation type: {simulation_type}")

    def update(self, forces: list[ForceFunc], dt: float, time: float|None = None) -> None:
        self._update_impl(forces, dt, time)
        return
    def copy(self) -> Particle:
        return Particle(
            mass=self.mass,
            position=self.position,
            velocity=self.velocity,
            simulation_type=self.simulation_type,
        )

    def _euler_update(self, forces: list[ForceFunc], dt: float, time: float|None = None) -> None:
        acceleration = sum_vec3(force(self, time) for force in forces) / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        return

    def _compute_expliced_acceleration(
        self,
        forces: list[ForceFunc],
        position: Vec3,
        velocity: Vec3,
        time: float|None = None
    ) -> Vec3:
        state = Particle(
            mass=self.mass,
            position=position,
            velocity=velocity,
            simulation_type=self.simulation_type,
        )
        total_force = sum_vec3(force(state, time) for force in forces)
        return total_force / self.mass

    def _rk_iteration(
        self,
        forces: list[ForceFunc],
        dt: float,
        dxdt: Vec3,
        dvdt: Vec3,
        time: float|None = None
    ) -> tuple[Vec3, Vec3]:
        # Em cada estágio, RK4 avalia f(x, v) = (v, a(x, v)).
        next_dxdt = self.velocity + dvdt * dt
        next_dvdt = self._compute_expliced_acceleration(
            forces,
            self.position + dxdt * dt,
            self.velocity + dvdt * dt,
            time
        )
        return next_dxdt, next_dvdt

    def _rk4_update(self, forces: list[ForceFunc], dt: float, time: float|None = None) -> None:
        half_dt = dt / 2.0
        vector_zero = Vec3(0, 0, 0)

        # primeira interação
        k1_dxdt, k1_dvdt = self._rk_iteration(
            forces,
            half_dt,
            vector_zero,
            vector_zero,
            time
        )
        # segunda interação
        k2_dxdt, k2_dvdt = self._rk_iteration(
            forces,
            half_dt,
            k1_dxdt,
            k1_dvdt,
            time
        )
        # terceira interação
        k3_dxdt, k3_dvdt = self._rk_iteration(
            forces,
            half_dt,
            k2_dxdt,
            k2_dvdt,
            time
        )
        # quarta interação
        k4_dxdt, k4_dvdt = self._rk_iteration(
            forces,
            dt,
            k3_dxdt,
            k3_dvdt,
            time
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
