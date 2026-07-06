from __future__ import annotations

from typing import Callable

from .linear_algebra import Vec3
from .particle import ForceFunc, Particle, SimulationTypes

type PairForceFunc = Callable[[Particle, Particle, float | None], Vec3]
type SystemForceFunc = PairForceFunc
type SystemUpdateFunc = Callable[
    [list[ForceFunc], list[PairForceFunc], float, float | None],
    None,
]


class ParticleSystem:
    particles: list[Particle]
    _simulation_type: SimulationTypes
    _update_impl: SystemUpdateFunc

    def __init__(
        self,
        particles: list[Particle],
        simulation_type: SimulationTypes = "RK4",
    ) -> None:
        if len(particles) == 0:
            raise ValueError("ParticleSystem requires at least one particle")

        self.particles = list(particles)
        self.simulation_type = simulation_type

    def __repr__(self) -> str:
        return (
            "ParticleSystem("
            f"particles={self.particles}, "
            f"simulation_type={self.simulation_type}"
            ")"
        )

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
    ) -> SystemUpdateFunc:
        if simulation_type == "Euler":
            return self._euler_update

        if simulation_type == "RK4":
            return self._rk4_update

        raise ValueError(f"Unsupported simulation type: {simulation_type}")

    def copy(self) -> ParticleSystem:
        return ParticleSystem(
            particles=[particle.copy() for particle in self.particles],
            simulation_type=self.simulation_type,
        )

    def kinetic_energy(self) -> float:
        total_energy = 0.0
        for particle in self.particles:
            total_energy += particle.kinetic_energy()
        return total_energy

    def update(
        self,
        dt: float,
        external_forces: list[ForceFunc] | None = None,
        pair_forces: list[PairForceFunc] | None = None,
        time: float | None = None,
    ) -> None:
        _external_forces = external_forces or []
        _pair_forces = pair_forces or []
        self._update_impl(_external_forces, _pair_forces, dt, time)

    def compute_total_forces(
        self,
        external_forces: list[ForceFunc] | None = None,
        pair_forces: list[PairForceFunc] | None = None,
        time: float | None = None,
    ) -> list[Vec3]:
        return self._compute_total_forces(
            particles=self.particles,
            external_forces=external_forces or [],
            pair_forces=pair_forces or [],
            time=time,
        )

    def _compute_total_forces(
        self,
        particles: list[Particle],
        external_forces: list[ForceFunc],
        pair_forces: list[PairForceFunc],
        time: float | None = None,
    ) -> list[Vec3]:
        total_forces = [Vec3(0.0, 0.0, 0.0) for _ in particles]

        for i, particle in enumerate(particles):
            for force in external_forces:
                total_forces[i] += force(particle, time)

        n_particles = len(particles)
        for i in range(n_particles):
            particle_i = particles[i]
            for j in range(i + 1, n_particles):
                particle_j = particles[j]
                for pair_force in pair_forces:
                    force_on_i = pair_force(particle_i, particle_j, time)
                    total_forces[i] += force_on_i
                    total_forces[j] -= force_on_i

        return total_forces

    def _compute_accelerations(
        self,
        positions: list[Vec3],
        velocities: list[Vec3],
        external_forces: list[ForceFunc],
        pair_forces: list[PairForceFunc],
        time: float | None = None,
    ) -> list[Vec3]:
        particles = [
            Particle(
                mass=particle.mass,
                position=position,
                velocity=velocity,
                simulation_type=self.simulation_type,
            )
            for particle, position, velocity in zip(
                self.particles,
                positions,
                velocities,
                strict=True,
            )
        ]
        total_forces = self._compute_total_forces(
            particles=particles,
            external_forces=external_forces,
            pair_forces=pair_forces,
            time=time,
        )
        return [
            force / particle.mass
            for particle, force in zip(particles, total_forces, strict=True)
        ]

    def _state_derivative(
        self,
        positions: list[Vec3],
        velocities: list[Vec3],
        external_forces: list[ForceFunc],
        pair_forces: list[PairForceFunc],
        time: float | None = None,
    ) -> tuple[list[Vec3], list[Vec3]]:
        accelerations = self._compute_accelerations(
            positions=positions,
            velocities=velocities,
            external_forces=external_forces,
            pair_forces=pair_forces,
            time=time,
        )
        return velocities, accelerations

    def _advance_state(
        self,
        values: list[Vec3],
        derivatives: list[Vec3],
        scale: float,
    ) -> list[Vec3]:
        return [
            value + derivative * scale
            for value, derivative in zip(values, derivatives, strict=True)
        ]

    def _advance_time(
        self,
        time: float | None,
        dt: float,
    ) -> float | None:
        if time is None:
            return None
        return time + dt

    def _euler_update(
        self,
        external_forces: list[ForceFunc],
        pair_forces: list[PairForceFunc],
        dt: float,
        time: float | None = None,
    ) -> None:
        total_forces = self._compute_total_forces(
            particles=self.particles,
            external_forces=external_forces,
            pair_forces=pair_forces,
            time=time,
        )

        for particle, force in zip(self.particles, total_forces, strict=True):
            particle.velocity += (force / particle.mass) * dt

        for particle in self.particles:
            particle.position += particle.velocity * dt

    def _rk4_update(
        self,
        external_forces: list[ForceFunc],
        pair_forces: list[PairForceFunc],
        dt: float,
        time: float | None = None,
    ) -> None:
        positions = [particle.position.copy() for particle in self.particles]
        velocities = [particle.velocity.copy() for particle in self.particles]
        half_dt = dt / 2.0

        k1_dr, k1_dv = self._state_derivative(
            positions,
            velocities,
            external_forces,
            pair_forces,
            time,
        )

        k2_dr, k2_dv = self._state_derivative(
            self._advance_state(positions, k1_dr, half_dt),
            self._advance_state(velocities, k1_dv, half_dt),
            external_forces,
            pair_forces,
            self._advance_time(time, half_dt),
        )

        k3_dr, k3_dv = self._state_derivative(
            self._advance_state(positions, k2_dr, half_dt),
            self._advance_state(velocities, k2_dv, half_dt),
            external_forces,
            pair_forces,
            self._advance_time(time, half_dt),
        )

        k4_dr, k4_dv = self._state_derivative(
            self._advance_state(positions, k3_dr, dt),
            self._advance_state(velocities, k3_dv, dt),
            external_forces,
            pair_forces,
            self._advance_time(time, dt),
        )

        for i, particle in enumerate(self.particles):
            particle.position = positions[i] + (
                k1_dr[i]
                + k2_dr[i] * 2.0
                + k3_dr[i] * 2.0
                + k4_dr[i]
            ) * (dt / 6.0)
            particle.velocity = velocities[i] + (
                k1_dv[i]
                + k2_dv[i] * 2.0
                + k3_dv[i] * 2.0
                + k4_dv[i]
            ) * (dt / 6.0)
