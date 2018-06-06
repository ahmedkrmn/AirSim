#pragma once

#include "CoreMinimal.h"
#include "PawnSimApi.h"
#include "vehicles/multirotor/MultiRotor.hpp"
#include "vehicles/multirotor/MultiRotorParams.hpp"
#include "physics//Kinematics.hpp"
#include "common/Common.hpp"
#include "common/CommonStructs.hpp"
#include "ManualPoseController.h"


class MultirotorPawnSimApi : public PawnSimApi
{
public:
    typedef msr::airlib::real_T real_T;
    typedef msr::airlib::Utils Utils;
    typedef msr::airlib::MultiRotor MultiRotor;
    typedef msr::airlib::StateReporter StateReporter;
    typedef msr::airlib::UpdatableObject UpdatableObject;
    typedef msr::airlib::Pose Pose;


public:
    virtual ~MultirotorPawnSimApi() = default;

    //VehicleSimApiBase interface
    //implements game interface to update pawn
    MultirotorPawnSimApi(APawn* pawn, const NedTransform& global_transform, CollisionSignal& collision_signal,
        const std::map<std::string, APIPCamera*>& cameras, UClass* pip_camera_class, UParticleSystem* collision_display_template,
        UManualPoseController* manual_pose_controller, const GeoPoint& home_geopoint);
    virtual void updateRenderedState(float dt) override;
    virtual void updateRendering(float dt) override;

    //PhysicsBody interface
    //this just wrapped around MultiRotor physics body
    virtual void reset() override;
    virtual void update() override;
    virtual void reportState(StateReporter& reporter) override;
    virtual UpdatableObject* getPhysicsBody() override;

    virtual void setPose(const Pose& pose, bool ignore_collision) override;
    virtual const msr::airlib::Kinematics::State* getGroundTruthKinematics() const override;
    virtual const msr::airlib::Environment* getGroundTruthEnvironment() const override;

    virtual std::string getLogLine() const override;

    msr::airlib::MultirotorApiBase* getVehicleApi()
    {
        return vehicle_api_.get();
    }


private:
    std::unique_ptr<msr::airlib::MultirotorApiBase> vehicle_api_;
    std::unique_ptr<msr::airlib::MultiRotorParams> vehicle_params_;
    UManualPoseController* manual_pose_controller_;

    std::unique_ptr<MultiRotor> phys_vehicle_;
    struct RotorInfo {
        real_T rotor_speed = 0;
        int rotor_direction = 0;
        real_T rotor_thrust = 0;
        real_T rotor_control_filtered = 0;
    };
    unsigned int rotor_count_;
    std::vector<RotorInfo> rotor_info_;

    //show info on collision response from physics engine
    CollisionResponse collision_response;

    //when pose needs to set from non-physics thread, we set it as pending
    bool pending_pose_collisions_;
    enum class PendingPoseStatus {
        NonePending, RenderStatePending, RenderPending
    } pending_pose_status_;
    Pose pending_phys_pose_; //force new pose through API

    //reset must happen while World is locked so its async task initiated from API thread
    bool reset_pending_;
    bool did_reset_;
    std::packaged_task<void()> reset_task_;

    Pose last_phys_pose_; //for trace lines showing vehicle path
    std::vector<std::string> vehicle_api_messages_;
};