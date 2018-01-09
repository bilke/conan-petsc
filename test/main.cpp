#include <petscts.h>

static const char help[] = "PETSc test program.";

int main(int argc,char *argv[]) {
  PetscErrorCode ierr;
  TS ts;

  ierr = PetscInitialize(&argc,&argv,0,help);
  CHKERRQ(ierr);
  ierr = TSCreate(PETSC_COMM_WORLD,&ts);
  CHKERRQ(ierr);
  ierr = TSSetFromOptions(ts);
  CHKERRQ(ierr);
  ierr = TSDestroy(&ts);
  CHKERRQ(ierr);
  ierr = PetscFinalize();
  CHKERRQ(ierr);
  return 0;
}
