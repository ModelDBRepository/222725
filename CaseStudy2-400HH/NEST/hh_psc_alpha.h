
#ifndef HH_PSC_ALPHA_H
#define HH_PSC_ALPHA_H

// Generated includes:
#include "config.h"

#ifdef HAVE_GSL

// External includes:
#include <gsl/gsl_errno.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_odeiv.h>
#include <gsl/gsl_sf_exp.h>

// Includes from nestkernel:
#include "archiving_node.h"
#include "connection.h"
#include "event.h"
#include "nest_types.h"
#include "recordables_map.h"
#include "ring_buffer.h"
#include "universal_data_logger.h"

namespace nest
{
extern "C" int hh_psc_alpha_dynamics( double, const double*, double*, void* );


class hh_psc_alpha : public Archiving_Node
{

public:
  hh_psc_alpha();
  hh_psc_alpha( const hh_psc_alpha& );
  ~hh_psc_alpha();

  using Node::handle;
  using Node::handles_test_event;

  port send_test_event( Node&, rport, synindex, bool );

  void handle( SpikeEvent& );
  void handle( CurrentEvent& );
  void handle( DataLoggingRequest& );

  port handles_test_event( SpikeEvent&, rport );
  port handles_test_event( CurrentEvent&, rport );
  port handles_test_event( DataLoggingRequest&, rport );

  double_t get_potential( Time const& ) const;

  void set_potential( Time const&, double_t );

  void get_status( DictionaryDatum& ) const;
  void set_status( const DictionaryDatum& );

private:
  void init_state_( const Node& proto );
  void init_buffers_();
  void calibrate();
  void update( Time const&, const long_t, const long_t );

  // END Boilerplate function declarations ----------------------------

  // Friends --------------------------------------------------------

  // make dynamics function quasi-member
  friend int hh_psc_alpha_dynamics( double, const double*, double*, void* );

  // The next two classes need to be friend to access the State_ class/member
  friend class RecordablesMap< hh_psc_alpha >;
  friend class UniversalDataLogger< hh_psc_alpha >;

private:
  // ----------------------------------------------------------------

  //! Independent parameters
  struct Parameters_
  {
    double_t t_ref_; //!< refractory time in ms
    double_t g_Na;   //!< Sodium Conductance in nS
    double_t g_K;    //!< Potassium Conductance in nS
    double_t g_L;    //!< Leak Conductance in nS
    double_t C_m;    //!< Membrane Capacitance in pF
    double_t E_Na;   //!< Sodium Reversal Potential in mV
    double_t E_K;    //!< Potassium Reversal Potential in mV
    double_t E_L;    //!< Leak reversal Potential (aka resting potential) in mV
    double_t tau_synE; //!< Synaptic Time Constant Excitatory Synapse in ms
    double_t tau_synI; //!< Synaptic Time Constant for Inhibitory Synapse in ms
    double_t I_e;      //!< Constant Current in pA

    Parameters_(); //!< Sets default parameter values

    void get( DictionaryDatum& ) const; //!< Store current values in dictionary
    void set( const DictionaryDatum& ); //!< Set values from dicitonary
  };

public:
  // ----------------------------------------------------------------

  struct State_
  {

    enum StateVecElems
    {
      V_M = 0,
      HH_M,   // 1
      HH_H,   // 2
      HH_N,   // 3
      DI_EXC, // 4
      I_EXC,  // 5
      DI_INH, // 6
      I_INH,  // 7
      STATE_VEC_SIZE
    };


    //! neuron state, must be C-array for GSL solver
    double_t y_[ STATE_VEC_SIZE ];
    int_t r_; //!< number of refractory steps remaining

    State_( const Parameters_& ); //!< Default initialization
    State_( const State_& );
    State_& operator=( const State_& );

    void get( DictionaryDatum& ) const;
    void set( const DictionaryDatum& );
  };

  // ----------------------------------------------------------------

private:
  struct Buffers_
  {
    Buffers_( hh_psc_alpha& );                  //!<Sets buffer pointers to 0
    Buffers_( const Buffers_&, hh_psc_alpha& ); //!<Sets buffer pointers to 0

    //! Logger for all analog data
    UniversalDataLogger< hh_psc_alpha > logger_;

    RingBuffer spike_exc_;
    RingBuffer spike_inh_;
    RingBuffer currents_;

    gsl_odeiv_step* s_;    //!< stepping function
    gsl_odeiv_control* c_; //!< adaptive stepsize control function
    gsl_odeiv_evolve* e_;  //!< evolution function
    gsl_odeiv_system sys_; //!< struct describing system

    // IntergrationStep_ should be reset with the neuron on ResetNetwork,
    // but remain unchanged during calibration. Since it is initialized with
    // step_, and the resolution cannot change after nodes have been created,
    // it is safe to place both here.
    double_t step_;          //!< step size in ms
    double IntegrationStep_; //!< current integration time step, updated by GSL

    double_t I_stim_;
  };

  // ----------------------------------------------------------------

  struct Variables_
  {
    double_t PSCurrInit_E_;

    double_t PSCurrInit_I_;

    int_t RefractoryCounts_;
  };

  // Access functions for UniversalDataLogger -------------------------------

  //! Read out state vector elements, used by UniversalDataLogger
  template < State_::StateVecElems elem >
  double_t
  get_y_elem_() const
  {
    return S_.y_[ elem ];
  }

  // ----------------------------------------------------------------

  Parameters_ P_;
  State_ S_;
  Variables_ V_;
  Buffers_ B_;

  //! Mapping of recordables names to access functions
  static RecordablesMap< hh_psc_alpha > recordablesMap_;
};


inline port
hh_psc_alpha::send_test_event( Node& target,
  rport receptor_type,
  synindex,
  bool )
{
  SpikeEvent e;
  e.set_sender( *this );

  return target.handles_test_event( e, receptor_type );
}


inline port
hh_psc_alpha::handles_test_event( SpikeEvent&, rport receptor_type )
{
  if ( receptor_type != 0 )
    throw UnknownReceptorType( receptor_type, get_name() );
  return 0;
}

inline port
hh_psc_alpha::handles_test_event( CurrentEvent&, rport receptor_type )
{
  if ( receptor_type != 0 )
    throw UnknownReceptorType( receptor_type, get_name() );
  return 0;
}

inline port
hh_psc_alpha::handles_test_event( DataLoggingRequest& dlr, rport receptor_type )
{
  if ( receptor_type != 0 )
    throw UnknownReceptorType( receptor_type, get_name() );
  return B_.logger_.connect_logging_device( dlr, recordablesMap_ );
}

inline void
hh_psc_alpha::get_status( DictionaryDatum& d ) const
{
  P_.get( d );
  S_.get( d );
  Archiving_Node::get_status( d );

  ( *d )[ names::recordables ] = recordablesMap_.get_list();
}

inline void
hh_psc_alpha::set_status( const DictionaryDatum& d )
{
  Parameters_ ptmp = P_; // temporary copy in case of errors
  ptmp.set( d );         // throws if BadProperty
  State_ stmp = S_;      // temporary copy in case of errors
  stmp.set( d );         // throws if BadProperty

  // We now know that (ptmp, stmp) are consistent. We do not
  // write them back to (P_, S_) before we are also sure that
  // the properties to be set in the parent class are internally
  // consistent.
  Archiving_Node::set_status( d );

  // if we get here, temporaries contain consistent set of properties
  P_ = ptmp;
  S_ = stmp;
}

} // namespace

#endif // HAVE_GSL
#endif // HH_PSC_ALPHA_H
