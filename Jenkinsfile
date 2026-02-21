pipeline {
    agent any

    parameters {
        string(name: 'LIVE_SERVER_BASE', description: 'Base path for live server (e.g. /home/amia/amia_server/server/)')
        string(name: 'TEST_SERVER_BASE', description: 'Base path for test server (e.g. /home/amia/amia_server/test_server/)')
        string(name: 'DEV_SERVER_BASE', description: 'Base path for dev server (e.g. /home/amia/dev_server/server/)')
        string(name: 'NWSYNC_PATH', description: 'Path to NWSync directory (e.g. /home/amia/amia_server/nwsync_test)')
        string(name: 'DOCKER_COMPOSE_PATH', description: 'Path to docker compose directory (e.g. /home/amia/amia_server)')
        choice(name: 'BUILD_ALL', choices: ['No', 'Yes'], description: 'Pack all haks regardless of changes')
        choice(name: 'DEPLOY_ALL', choices: ['No', 'Yes'], description: 'Deploy haks to live server')
        choice(name: 'DEPLOY_TEST', choices: ['No', 'Yes'], description: 'Deploy haks to test server')
        choice(name: 'DEPLOY_DEV', choices: ['No', 'Yes'], description: 'Deploy haks to dev server')
    }

    environment {
        CHANGES = 'false'
    }

    stages {
        stage('Check for changes') {
            when {
                not {
                    changeset "src/**/**/**"
                }
                expression {
                    return params.BUILD_ALL == 'No'
                }
            }
            steps {
                echo "Nothing to do."
            }
        }

        stage('Pack Amia Top') {
            when {
                changeset "src/hak/amia_top/**/**"
            }
            steps {
                echo 'Packing Amia top'
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_top"
                }
            }
        }

        stage('Pack Amia Parts') {
            when {
                changeset "src/hak/amia_parts/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_parts"
                }
            }
        }

        stage('Pack Amia Races') {
            when {
                changeset "src/hak/amia_races/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_races"
                }
            }
        }

        stage('Pack Amia amia_plc') {
            when {
                changeset "src/hak/amia_plc/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_plc"
                }
            }
        }

        stage('Pack Amia Items') {
            when {
                changeset "src/hak/amia_items/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_items"
                }
            }
        }

        stage('Pack Amia Rest') {
            when {
                changeset "src/hak/amia_rest/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_rest"
                }
            }
        }

        stage('Pack Amia A') {
            when {
                changeset "src/hak/amia_a/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_a"
                }
            }
        }

        stage('Pack Amia B') {
            when {
                changeset "src/hak/amia_b/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_b"
                }
            }
        }

        stage('Pack Amia C') {
            when {
                changeset "src/hak/amia_c/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_c"
                }
            }
        }

        stage('Pack Amia D') {
            when {
                changeset "src/hak/amia_d/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_d"
                }
            }
        }

        stage('Pack Amia Music') {
            when {
                changeset "src/hak/amia_music/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_music"
                }
            }
        }

        stage('Pack Amia Override') {
            when {
                changeset "src/hak/amia_override/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_override"
                }
            }
        }

        stage('Pack Amia Override 2') {
            when {
                changeset "src/hak/amia_override2/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_override2"
                }
            }
        }

        stage('Pack Amia Creature') {
            when {
                changeset "src/hak/amia_creature/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_creature"
                }
            }
        }

        stage('Pack Amia Creature 2') {
            when {
                changeset "src/hak/amia_creature2/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_creature2"
                }
            }
        }

        stage('Pack Amia Skybox') {
            when {
                changeset "src/hak/amia_skybox/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_skybox"
                }
            }
        }

        stage('Pack Amia Weapons') {
            when {
                changeset "src/hak/amia_weapons/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_weapons"
                }
            }
        }

        stage('Pack Amia Nui') {
            when {
                changeset "src/hak/amia_nui/**/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh hak amia_nui"
                }
            }
        }

        stage('Pack Amia TLK') {
            when {
                changeset "src/tlk/amia_tlk/tlk/**"
            }
            steps {
                script {
                    sh "chmod +x pack.sh && dos2unix pack.sh && ./pack.sh tlk tlk"
                }
            }
        }

        stage('Pack everything') {
            when {
                expression {
                    return params.BUILD_ALL == 'Yes'
                }
            }
            steps {
                script {
                    sh "chmod +x linux-pack-all.sh && dos2unix linux-pack-all.sh && ./linux-pack-all.sh"
                }
            }
        }

        stage('Deploy-Haks') {
            when {
                expression {
                    return params.DEPLOY_ALL == 'Yes'
                }
            }
            steps {
                script {
                    if (!params.LIVE_SERVER_BASE?.trim()) {
                        error "LIVE_SERVER_BASE parameter is required for live deployment but was not set."
                    }
                    sh """
                        chmod +x deploy.sh linux-pack-all.sh cleanup.sh
                        dos2unix deploy.sh linux-pack-all.sh cleanup.sh
                        ./linux-pack-all.sh
                        ./deploy.sh ${params.LIVE_SERVER_BASE}
                        ./cleanup.sh
                    """
                }
            }
        }

        stage('Deploy-Haks-Test') {
            when {
                expression {
                    return params.DEPLOY_TEST == 'Yes'
                }
            }
            steps {
                script {
                    if (!params.TEST_SERVER_BASE?.trim()) {
                        error "TEST_SERVER_BASE parameter is required for test deployment but was not set."
                    }
                    sh """
                        chmod +x deploy.sh linux-pack-all.sh cleanup.sh
                        dos2unix deploy.sh linux-pack-all.sh cleanup.sh
                        ./linux-pack-all.sh
                        ./deploy.sh ${params.TEST_SERVER_BASE}
                        ./cleanup.sh
                    """
                }
            }
        }

        stage('Deploy-Haks-Dev') {
            when {
                expression {
                    return params.DEPLOY_DEV == 'Yes'
                }
            }
            steps {
                script {
                    if (!params.DEV_SERVER_BASE?.trim()) {
                        error "DEV_SERVER_BASE parameter is required for dev deployment but was not set."
                    }
                    sh """
                        chmod +x deploy.sh linux-pack-all.sh cleanup.sh
                        dos2unix deploy.sh linux-pack-all.sh cleanup.sh
                        ./linux-pack-all.sh
                        ./deploy.sh ${params.DEV_SERVER_BASE}
                        ./cleanup.sh
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Finalizing results.'
        }
        success {
            archiveArtifacts artifacts: '*.hak', followSymlinks: false, allowEmptyArchive: true
            archiveArtifacts artifacts: '*.tlk', followSymlinks: false, allowEmptyArchive: true
            archiveArtifacts artifacts: '*.zip', followSymlinks: false, allowEmptyArchive: true
            echo 'Build complete'
            script {
				if (params.DEPLOY_TEST == 'Yes') {
					if (!params.NWSYNC_PATH?.trim() || !params.TEST_SERVER_BASE?.trim()) {
						echo 'WARNING: NWSYNC_PATH or TEST_SERVER_BASE not set. Skipping NWSync Update.'
					} else {
						echo 'Updating NWSync data...'
						sh """#!/bin/bash
							set -euo pipefail
							cd ${params.NWSYNC_PATH}
							if [ -f ./bin/nwn_nwsync_write ] && [ -f ${params.TEST_SERVER_BASE}/modules/Amia.mod ]; then
								./bin/nwn_nwsync_write --description="Amia Server Data" data/ ${params.TEST_SERVER_BASE}/modules/Amia.mod
							else
								echo "NWSync files not found, skipping..."
							fi
						"""
					}
				}
				else {
					echo 'DEPLOY_TEST not selected. Skipping NWSync Update.'
				}
            }
            script {
				if (params.DEPLOY_TEST == 'Yes') {
					if (!params.DOCKER_COMPOSE_PATH?.trim() || !params.NWSYNC_PATH?.trim()) {
						echo 'WARNING: DOCKER_COMPOSE_PATH or NWSYNC_PATH not set. Skipping Restart.'
					} else {
						echo 'Resetting test-server via docker compose...'
						sh """#!/bin/bash
							set -euo pipefail
							cd ${params.DOCKER_COMPOSE_PATH}
							if command -v docker &> /dev/null; then
								docker compose stop test-server || true
								docker compose rm -f test-server || true
								docker compose up -d test-server database-test nwsync-test webui
							else
								echo "docker not found, skipping..."
							fi
							cd ${params.NWSYNC_PATH}
							./bin/nwn_nwsync_prune data
						"""
					}
				}
				else {
					echo 'DEPLOY_TEST not selected. Skipping Restart.'
				}
            }
        }
    }
}
