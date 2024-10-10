import React from 'react';

const styles = {
  Subject: {
    top: '232px',
    left: '320px',
    width: '384px',
    height: '60px',
    backgroundColor: '#d0d3f5',
    borderRadius: '8px',
    boxShadow: '0px 4px 12px rgba(0,0,0,0.25)',
  },
};

const Subject = (props) => {
  return (
    <div style={styles.Card}>
      {props.children}
    </div>
  );
};

export default Subject;
