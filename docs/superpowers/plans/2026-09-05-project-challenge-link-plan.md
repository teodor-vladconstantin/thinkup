# Proiecte legate de Challenge-uri reale — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the free-text project category (`areaOfImplementation`) with a real link to one of 4 `Challenge` records, making a project the vehicle through which a student participates in a challenge — unifying with the existing (currently unused) `Submissions` grading system.

**Architecture:** `Project` gains a `challengeId` field (backend entity + encoder + routes), replacing `areaOfImplementation` everywhere. A new admin page lets mentors manage `Challenge` records through the already-existing but previously unused backend CRUD routes. `Submission` gains a `projectId`, and a new project-based grading route creates one `Submission` per project admin (team grading). `DeadlineBanner` switches from "have I been graded" to "do I have a project on this challenge".

**Tech Stack:** Flask + DynamoDB (Alternator) backend, Next.js/React frontend, deployed via `docker compose build/up` on the VPS at `91.200.121.128` (no CI/CD).

## Global Constraints

- **No test framework exists in this repo** (confirmed: no pytest, no jest, no test config anywhere). Every "test cycle" step in this plan means: deploy to the real running containers on the VPS, exercise the real endpoint with `curl` against `https://thinkupacademy.ro` using real or throwaway test data, verify the actual response/DB state, then delete any throwaway data created for the test. This matches how every prior fix on this VPS has been verified (see git log). Do not introduce a test framework as part of this plan.
- VPS access: `ssh 91.200.121.128 "<command>"`. Repo at `/root/thinkup`. Backend deploy: `cd /root/thinkup/platform-backend && docker compose build backend && docker compose up -d backend`. Frontend deploy: `cd /root/thinkup/platform-backend && docker compose build frontend && docker compose up -d frontend` (frontend service also lives under the `platform-backend/docker-compose.yml`, confirmed via `docker compose config --services`).
- Get a test Bearer token any time with: `curl -s https://thinkupacademy.ro/api/token | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])"`.
- Real user ids already in production for testing: `108725634211690813513` (Teodor Vlad Constantin, owns project `mtega0tmtzvbkcudjoh`), `113528018155821801130` (owns project `mtmntkh9asjptglks8`).
- Commit after every task with the `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` / `Claude-Session:` trailer already used in every commit on this repo — copy the exact trailer format from `git log -1`.
- Never edit `.env` directly with shell commands (blocked by the security classifier in this environment on a prior task) — if a task needs new env vars, ask the user to add them, or use the DB/API directly instead.
- Every commit message template below uses `<session-url>` as a literal placeholder — replace it with the executing session's own `Claude-Session:` URL (visible in that session's own system context) before running the commit. This is not a TBD: it is a real value that exists at execution time and varies per session, the same way every prior commit on this repo carries its author session's URL.

---

## Piece 1 — Project↔Challenge link (foundation, implement and land first, solo)

### Task 1.1: Backend — `Project` entity + encoder use `challengeId` instead of `areaOfImplementation`

**Files:**
- Modify: `platform-backend/src/model/entity/project.py`
- Modify: `platform-backend/src/model/entity/jsonencoders/project_encoder.py`

**Interfaces:**
- Produces: `Project.__init__(..., challengeId: str, ...)` (same position as the old `areaOfImplementation` param), `get_challengeId()`, `set_challengeId(challengeId)`. `ProjectEncoder.toJSON(project)` now emits a `challengeId` key instead of `areaOfImplementation`.

- [ ] **Step 1: Edit `project.py`** — replace the `areaOfImplementation` parameter and its getter/setter with `challengeId`:

```python
class Project:
    def __init__(self, id: str, name: str, searchTerm: str, description: str, thumbnail, thumbnail_extension,
                 createdBy: str, adminList: list, creationDate, challengeId: str, goals: Goals,
                 materials: Materials, pitchId: str, settings: dict, projectReviews: ProjectReviews, mentor_feedback: list,
                 photos: list = None):
        self.__id = id
        self.__name = name
        self.__searchTerm = searchTerm
        self.__createdBy = createdBy
        self.__description = description
        self.__thumbnail = thumbnail
        self.__thumbnail_extension = thumbnail_extension
        self.__creationDate = creationDate
        self.__challengeId = challengeId
        self.__goals = goals
        self.__materials = materials
        self.__pitchId = pitchId
        self.__adminList = adminList
        self.__settings = settings
        self.__projectReviews = projectReviews
        self.__mentor_feedback = mentor_feedback
        self.__photos = photos if photos is not None else []
```

Replace `get_areOfImplementation`/`set_areOfImplementation` with:

```python
    def get_challengeId(self):
        return self.__challengeId

    def set_challengeId(self, challengeId: string):
        self.__challengeId = challengeId
```

Leave every other method untouched.

- [ ] **Step 2: Edit `project_encoder.py`** — replace the line `'areaOfImplementation': o.get_areOfImplementation(),` with `'challengeId': o.get_challengeId(),`. Also update the docstring JSON example at the bottom of the file (`"area_of_implementation": "Environment"` → `"challengeId": "challenge1"`).

- [ ] **Step 3: Compile-check on the VPS**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && python3 -m py_compile src/model/entity/project.py src/model/entity/jsonencoders/project_encoder.py && echo OK"
```
Expected: `OK`

- [ ] **Step 4: Commit** (do not build/deploy yet — Task 1.2 touches the same feature and should ship together)

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-backend/src/model/entity/project.py platform-backend/src/model/entity/jsonencoders/project_encoder.py && git commit -m "Project foloseste challengeId in loc de areaOfImplementation (entity+encoder)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

### Task 1.2: Backend — `view_projects.py` reads/writes `challengeId`, enforces one project per challenge per student

**Files:**
- Modify: `platform-backend/src/views/view_projects.py`
- Modify: `platform-backend/src/api/api_crud_projects.py`

**Interfaces:**
- Consumes: `Project(...)` constructor from Task 1.1, `apiProjects.getOwnedProjects(owner_id)` (existing, returns `{'projects': [...]}`, matches on `owner_id in project['adminList']`).
- Produces: `POST /projects/<id>` and `PUT /projects/<id>` now require `challengeId` in the JSON/form body (instead of `area_of_implementation`/`areaOfImplementation`), return `409` with a Romanian description if the user already has another project on that challenge.

- [ ] **Step 1: Edit `addProject` in `view_projects.py`** — add the duplicate-challenge check and switch the field name:

```python
@urlProject.route('/projects/<string:id>', methods=['POST'])
@require_auth(None)
# @Utils.check_project_token  # disabled: project creation no longer requires a token
def addProject(id: str):
    """Add a project

    Args:
        id (str): id of the project to add

    Returns:
        _type_: response
    """
    project_token = request.args.get('project_token')
    materials_obj = Materials([])
    goal = Goals([])
    projectJson = request.json

    created_by = projectJson['created_by']
    challenge_id = projectJson['challengeId']

    existing_projects = apiProjects.getOwnedProjects(created_by).get('projects', [])
    if any(p.get('challengeId') == challenge_id for p in existing_projects):
        abort(409, description="Ai deja un proiect pe acest challenge")

    projectReviews = ProjectReviews(projectJson['id'], 0, 0, [])
    projectObj = Project(projectJson['id'], projectJson['name'], str(projectJson['name']).lower(), projectJson['description'], "defaultThumbnailCIVIC1", ".png", created_by, [created_by], projectJson['creation_date'], challenge_id, goal, materials_obj, "pitchId#999", {"accept_reviews": True}, projectReviews, mentor_feedback, [])

    updateActivity(created_by, "create_project", 2)

    return apiProjects.addProject(project_token, projectObj)
```

- [ ] **Step 2: Edit `updateProject` in `view_projects.py`** — insert a duplicate-challenge check right after the existing authorization check (before `projectJson["created_by"] = projectUpdated["createdBy"]`):

```python
    if not (is_owner or is_admin):
         logger.warning(f"User {user_id} unauthorized to update project {id}")
         abort(403, description="You are not authorized to update this project")

    new_challenge_id = projectJson.get('challengeId')
    if new_challenge_id and new_challenge_id != projectUpdated.get('challengeId'):
        existing_projects = apiProjects.getOwnedProjects(user_id).get('projects', [])
        if any(p.get('challengeId') == new_challenge_id and p.get('id') != id for p in existing_projects):
            abort(409, description="Ai deja un proiect pe acest challenge")

    projectJson["created_by"] = projectUpdated["createdBy"]
```

- [ ] **Step 3: Edit `api_crud_projects.py::updateProject`** — change the field it copies from the incoming JSON:

```python
    try:
      projectToUpdate['challengeId'] = projectJson['challengeId']
    except KeyError:
      pass
```//(replaces the existing `areaOfImplementation` try/except block, same position)

- [ ] **Step 4: Compile-check**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && python3 -m py_compile src/views/view_projects.py src/api/api_crud_projects.py && echo OK"
```
Expected: `OK`

- [ ] **Step 5: Build and deploy backend**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && docker compose build backend && docker compose up -d backend"
```
Expected: `Image platform-backend-backend Built`, then `Container thinkup-app Started`.

- [ ] **Step 6: Verify on production with a throwaway Challenge (seeded directly in DB — Piece 2's admin UI doesn't exist yet)**

```bash
ssh 91.200.121.128 'bash -s' <<"REMOTE"
docker exec thinkup-app python3 -c "
import boto3
db = boto3.resource('dynamodb', endpoint_url='http://scylladb:8000', region_name='eu-central-1', aws_access_key_id='local', aws_secret_access_key='local')
db.Table('Challenges').put_item(Item={'id': 'plan-test-challenge-1', 'name': 'Plan Test Challenge', 'description': 'x', 'deadline': '2027-01-01T00:00:00', 'maxScore': 100, 'createdBy': '108725634211690813513', 'creationDate': '2026-09-05'})
print('seeded')
"
TOKEN=$(curl -s https://thinkupacademy.ro/api/token | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
OWNER="108725634211690813513"
TS=$(date +%s)
PID="plan-test-project-$TS"

echo "-- create project on the test challenge (expect 200) --"
curl -s -o /tmp/p1.json -w "HTTP:%{http_code}\n" -X POST "https://thinkupacademy.ro/projects/$PID" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d "{\"id\":\"$PID\",\"name\":\"Plan test\",\"challengeId\":\"plan-test-challenge-1\",\"creation_date\":\"05/9/2026\",\"description\":\"x\",\"created_by\":\"$OWNER\"}"
cat /tmp/p1.json; echo

echo "-- second project, same user, same challenge (expect 409) --"
PID2="plan-test-project-2-$TS"
curl -s -o /tmp/p2.json -w "HTTP:%{http_code}\n" -X POST "https://thinkupacademy.ro/projects/$PID2" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d "{\"id\":\"$PID2\",\"name\":\"Plan test 2\",\"challengeId\":\"plan-test-challenge-1\",\"creation_date\":\"05/9/2026\",\"description\":\"x\",\"created_by\":\"$OWNER\"}"
cat /tmp/p2.json; echo

echo "-- confirm challengeId stored on the first project --"
curl -s "https://thinkupacademy.ro/projects/$PID" | python3 -c "import sys,json; print(json.load(sys.stdin)['challengeId'])"

echo "-- cleanup: delete test project 1 (as owner) and the seeded challenge --"
curl -s -o /dev/null -w "delete HTTP:%{http_code}\n" -X DELETE "https://thinkupacademy.ro/projects/$PID" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "{\"created_by\":\"$OWNER\"}"
docker exec thinkup-app python3 -c "
import boto3
db = boto3.resource('dynamodb', endpoint_url='http://scylladb:8000', region_name='eu-central-1', aws_access_key_id='local', aws_secret_access_key='local')
db.Table('Challenges').delete_item(Key={'id': 'plan-test-challenge-1'})
print('challenge deleted')
"
rm -f /tmp/p1.json /tmp/p2.json
REMOTE
```
Expected: first create `HTTP:200`, second create `HTTP:409`, `challengeId` printed as `plan-test-challenge-1`, cleanup both `200`/`challenge deleted`.

- [ ] **Step 7: Commit**

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-backend/src/views/view_projects.py platform-backend/src/api/api_crud_projects.py && git commit -m "addProject/updateProject folosesc challengeId, un proiect per challenge per elev

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

### Task 1.3: Frontend — `NewProject`/`EditProject` pick a real Challenge instead of a hardcoded category

**Files:**
- Modify: `platform-frontend/src/pages/NewProject/index.js`
- Modify: `platform-frontend/src/pages/Projects/[id]/EditProject.js`

**Interfaces:**
- Consumes: `GET /challenges` → `{"challenges": [{id, name, description, deadline, maxScore, createdBy, creationDate}, ...]}` (existing route). `POST /projects/<id>` and `PUT /projects/<id>` now expect `challengeId` (Task 1.2).

- [ ] **Step 1: Edit `NewProject/index.js`** — remove the hardcoded `AreaOfImplementationOptions` array and the `AreaOfImplementation`/`value` state; fetch real challenges and track the selected challenge by name (display) while submitting its id:

Replace:
```jsx
    const [AreaOfImplementation, setAreaOfImplementation] = useState("Select");
    const [value, setFilterValue] = useState("Select");
```
with:
```jsx
    const [Challenges, setChallenges] = useState([]);
    const [SelectedChallengeName, setSelectedChallengeName] = useState("Select");
```

Add, right after the existing state declarations:
```jsx
    useEffect(() => {
        const fetchChallenges = async () => {
            try {
                const response = await apiClient.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges`
                );
                setChallenges(response.data.challenges || []);
            } catch (err) {
                console.log(err);
            }
        };
        fetchChallenges();
    }, []);
```
(`apiClient` and `useEffect` are already imported at the top of this file.)

Delete the `AreaOfImplementationOptions` array entirely and replace its only use with:
```jsx
    const ChallengeOptions = Challenges.map((challenge) => challenge.name);
```

In `CreateProject`, replace the validation line `AreaOfImplementation == "0"` with `SelectedChallengeName == "Select"`, and replace the request body:
```jsx
        const selectedChallenge = Challenges.find(
            (c) => c.name === SelectedChallengeName
        );
        if (!selectedChallenge) {
            showProjectError("Alege un challenge.");
            return;
        }
        try {
            const response = await apiClient.post(
                `${process.env.NEXT_PUBLIC_API_URL}/projects/${id}`,
                {
                    id: id,
                    name: ProjectName,
                    challengeId: selectedChallenge.id,
                    creation_date: date,
                    description: Description,
                    created_by: user.id,
                }
            );
```
(keep the existing `try`/`catch` wrapper and the rest of the function body unchanged — only the body object inside `apiClient.post` changes.)

Replace the commented-out `<SelectField ...>` block and the active one below it — delete the commented block entirely, and change the active one to:
```jsx
            <SelectField
                selectTitle="Challenge"
                width="250"
                value={SelectedChallengeName}
                setValue={(e) => {
                    setSelectedChallengeName(e);
                }}
                onChange={(e) => setSelectedChallengeName(e.target.value)}
                options={ChallengeOptions}
            />
```

- [ ] **Step 2: Edit `EditProject.js`** — same idea, but the initial value comes from the project being edited (`challengeId`, not a name), so track the id directly and derive the display name:

Replace:
```jsx
    const [AreaOfImplementation, setAreaOfImplementation] = useState("Select");
```
with:
```jsx
    const [Challenges, setChallenges] = useState([]);
    const [ChallengeId, setChallengeId] = useState(null);
```

Replace the body of `getProjectData`'s relevant line and the commented-out switch block:
```jsx
        setProjectTitle(response.data.name);
        setProjectDescription(response.data.description);
        setChallengeId(response.data.challengeId);
```
(delete the commented-out `switch (response.data.areaOfImplementation) { ... }` block below it entirely)

Replace the `useEffect` that calls `getProjectData()` to also fetch challenges:
```jsx
    useEffect(() => {
        getProjectData();
        const fetchChallenges = async () => {
            try {
                const response = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges`
                );
                setChallenges(response.data.challenges || []);
            } catch (err) {
                console.log(err);
            }
        };
        fetchChallenges();
    }, [id]);
```

Delete the `AreaOfImplementationOptions` array, replace with:
```jsx
    const ChallengeOptions = Challenges.map((challenge) => challenge.name);
    const SelectedChallengeName =
        Challenges.find((c) => c.id === ChallengeId)?.name || "Select";
```

In `EditProject` (the submit function), replace `areaOfImplementation: AreaOfImplementation,` with `challengeId: ChallengeId,` inside the `formdata.append("json", JSON.stringify({...}))` call.

Replace the `<SelectField ...>` JSX:
```jsx
                <SelectField
                    selectTitle="Challenge"
                    width="250"
                    value={SelectedChallengeName}
                    setValue={(name) => {
                        const match = Challenges.find((c) => c.name === name);
                        if (match) setChallengeId(match.id);
                    }}
                    onChange={() => {}}
                    options={ChallengeOptions}
                />
```

- [ ] **Step 3: Build check on the VPS** (inside the running frontend container, matches how this repo already verifies frontend changes)

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-frontend && docker exec thinkup-frontend npm run build 2>&1 | tail -30"
```
Expected: build completes, page list printed, no red error output (pre-existing lint warnings about `<img>` are fine and unrelated).

- [ ] **Step 4: Commit** (deploy happens together with Task 1.4, same feature)

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-frontend/src/pages/NewProject/index.js "platform-frontend/src/pages/Projects/[id]/EditProject.js" && git commit -m "NewProject/EditProject aleg un Challenge real, nu mai categorie hardcodata

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

### Task 1.4: Frontend — project cards/badges display the Challenge name with a stable color

**Files:**
- Modify: `platform-frontend/src/components/Cards/CategoryCard.js`
- Modify: `platform-frontend/styles/CategoryCard.module.css`
- Modify: `platform-frontend/src/components/Cards/ProjectCard.js`
- Modify: `platform-frontend/styles/ProjectCard.module.css`
- Modify: `platform-frontend/src/components/Tables/ProjectsTable.js`
- Modify: `platform-frontend/src/pages/Projects/[id]/index.js`

**Interfaces:**
- Consumes: `GET /challenges` (existing). `Project.challengeId` (Task 1.1/1.2).
- Produces: `CategoryCard`/`ProjectCard` accept a new `colorIndex` prop (0-3, the challenge's position in the full challenges list) instead of deriving color from the category text.

- [ ] **Step 1: Add 4 stable color classes to `CategoryCard.module.css`** — append (don't remove the existing `.Ecological`/`.Stem` rules, they're now unused but harmless):

```css
.ChallengeColor0 {
    background: #c98cde;
}

.ChallengeColor1 {
    background: #7eda98;
}

.ChallengeColor2 {
    background: #85acf8;
}

.ChallengeColor3 {
    background: #f6b93b;
}
```

- [ ] **Step 2: Edit `CategoryCard.js`** — use `colorIndex` instead of the category text for the CSS class:

```jsx
import React from "react";
import styles from "../../../styles/CategoryCard.module.css";

const CategoryCard = (props) => {
    return (
        <div
            className={
                styles.CategoryCard +
                " " +
                props.className +
                " " +
                styles["ChallengeColor" + (props.colorIndex ?? 0)]
            }
            onClick={() => {}}
        >
            {props.children}
        </div>
    );
};
export default CategoryCard;
```

- [ ] **Step 3: Same 4 classes in `ProjectCard.module.css`** — append after the existing `.Ecological`/`.Stem` rules:

```css
.ChallengeColor0 {
    background: #c98cde;
}

.ChallengeColor1 {
    background: #7eda98;
}

.ChallengeColor2 {
    background: #85acf8;
}

.ChallengeColor3 {
    background: #f6b93b;
}
```

- [ ] **Step 4: Edit `ProjectCard.js`** — same `colorIndex` change, replacing this block:

```jsx
                <p
                    className={
                        styles.ProjectCategory + " " + styles[props.category]
                    }
                >
                    {props.category}
                </p>
```
with:
```jsx
                <p
                    className={
                        styles.ProjectCategory +
                        " " +
                        styles["ChallengeColor" + (props.colorIndex ?? 0)]
                    }
                >
                    {props.category}
                </p>
```

- [ ] **Step 5: Edit `ProjectsTable.js`** — fetch challenges once, resolve each project's `challengeId` to a name + color index:

```jsx
import React, { useState, useEffect } from "react";
import styles from "../../../styles/ProjectsTable.module.css";
import ProjectCard from "../Cards/ProjectCard";
import NewProjectCard from "../Cards/NewProjectCard";
import { motion } from "framer-motion";
import { useRouter } from "next/router";
import ScrollContainer from "../Containers/ScrollContainer";
import axios from "axios";

const ProjectsTable = (props) => {
    const router = useRouter();
    const [Challenges, setChallenges] = useState([]);

    useEffect(() => {
        const fetchChallenges = async () => {
            try {
                const response = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges`
                );
                setChallenges(response.data.challenges || []);
            } catch (err) {
                console.log(err);
            }
        };
        fetchChallenges();
    }, []);

    if (props.data == undefined) return <></>;

    return (
        <div className={styles.ProjectsTableContainer}>
            <ScrollContainer
                className={styles.ProjectsTable + " " + props.className}
                onClick={() => {}}
            >
                {props.data.map((projectdata, index) => {
                    if (projectdata.addcard == true)
                        return (
                            <NewProjectCard
                                onClick={() => router.push("/NewProject")}
                                key={index}
                            />
                        );
                    const challengeIndex = Challenges.findIndex(
                        (c) => c.id === projectdata.challengeId
                    );
                    const challengeName =
                        challengeIndex >= 0
                            ? Challenges[challengeIndex].name
                            : "";
                    return (
                        <ProjectCard
                            title={projectdata.name}
                            animation_delay={index + 1}
                            key={index}
                            id={projectdata.id}
                            category={challengeName}
                            colorIndex={challengeIndex >= 0 ? challengeIndex : 0}
                            thumbnail={projectdata.thumbnail}
                            thumbnail_extension={projectdata.thumbnail_extension}
                        >
                            {projectdata.description}
                        </ProjectCard>
                    );
                })}
            </ScrollContainer>
            <div className={styles.ProjectsTableShadow}></div>
        </div>
    );
};

export default ProjectsTable;
```

- [ ] **Step 6: Edit `pages/Projects/[id]/index.js`** — fetch challenges, resolve the project's own `challengeId` to a name + color index, pass to `CategoryCard`:

Add state near the other `useState` calls:
```jsx
    const [Challenges, setChallenges] = useState([]);
```

Add a fetch effect (alongside whatever effect already loads `ProjectData` — add as its own `useEffect`):
```jsx
    useEffect(() => {
        const fetchChallenges = async () => {
            try {
                const response = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges`
                );
                setChallenges(response.data.challenges || []);
            } catch (err) {
                console.log(err);
            }
        };
        fetchChallenges();
    }, []);
```

Replace:
```jsx
                    <CategoryCard category={ProjectData.areaOfImplementation}>
                        {ProjectData.areaOfImplementation}
                    </CategoryCard>
```
with:
```jsx
                    <CategoryCard
                        colorIndex={Math.max(
                            0,
                            Challenges.findIndex(
                                (c) => c.id === ProjectData.challengeId
                            )
                        )}
                    >
                        {Challenges.find((c) => c.id === ProjectData.challengeId)
                            ?.name || ""}
                    </CategoryCard>
```

- [ ] **Step 7: Build check**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-frontend && docker exec thinkup-frontend npm run build 2>&1 | tail -30"
```
Expected: build completes, no new errors.

- [ ] **Step 8: Deploy frontend**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && docker compose build frontend && docker compose up -d frontend"
```
Expected: `Image platform-backend-frontend Built`, `Container thinkup-frontend Started`.

- [ ] **Step 9: Verify on production** — seed a throwaway challenge + project again (same pattern as Task 1.2 Step 6), then load the project page and the projects table and visually confirm (via `curl` on the underlying API responses, since there's no browser automation in this environment unless explicitly available) that `challengeId` round-trips and the frontend build contains the new `ChallengeColor` class names:

```bash
ssh 91.200.121.128 "docker exec thinkup-frontend grep -r 'ChallengeColor' .next/static/css/*.css | head -3"
```
Expected: at least one match, confirming the new CSS classes made it into the production build.

- [ ] **Step 10: Commit**

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-frontend/src/components/Cards/CategoryCard.js platform-frontend/styles/CategoryCard.module.css platform-frontend/src/components/Cards/ProjectCard.js platform-frontend/styles/ProjectCard.module.css platform-frontend/src/components/Tables/ProjectsTable.js "platform-frontend/src/pages/Projects/[id]/index.js" && git commit -m "Badge-ul de proiect afiseaza numele Challenge-ului, culoare pe pozitie

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

## Piece 1 checkpoint

Before starting Pieces 2-4 (which can run in parallel via subagents), confirm:
- [ ] `git log --oneline -4` on the VPS shows the 4 Piece 1 commits.
- [ ] `docker ps` shows `thinkup-app` and `thinkup-frontend` both freshly restarted and `Up`.
- [ ] No leftover `plan-test-*` projects or challenges in the DB (re-run the scan from earlier sessions: `docker exec thinkup-app python3 -c "..."` scanning `Projects`/`Challenges` tables for `plan-test` in the id).

Only after this checkpoint passes, dispatch Pieces 2, 3, 4 (each below is a self-contained brief a fresh subagent can execute against this same repo).

---

## Piece 2 — Challenges admin page (parallel-eligible after Piece 1 checkpoint)

### Task 2.1: Backend — restrict `POST/PUT/DELETE /challenges` to Mentors

**Files:**
- Modify: `platform-backend/src/views/view_challenges.py`

**Interfaces:**
- Consumes: `dbCrudUsers` pattern from `view_warnings.py` (`setup.startSetup('Users')`, `.getUser(id)` returns a dict with a `role` key).
- Produces: `addChallenge`/`updateChallenge`/`deleteChallenge` now require a `created_by` field in the JSON body that resolves to a User with `role == 'Mentor'`, otherwise `403`.

- [ ] **Step 1: Add a Users table reference** — after `dbCrudChallenges = setup.startSetup('Challenges')`, add:

```python
dbCrudUsers = setup.startSetup('Users')


def _require_mentor(user_id):
    """Abort with 403 unless user_id resolves to a User with role Mentor."""
    if not user_id:
        abort(403, description="created_by is required")
    user = dbCrudUsers.getUser(user_id)
    if not user or "ErrorMessage" in user:
        abort(403, description="You are not authorized to manage challenges")
    if user.get('role') != 'Mentor':
        abort(403, description="Only mentors can manage challenges")
```

- [ ] **Step 2: Call `_require_mentor` in `addChallenge`** — right after `challengeJson = request.json`:

```python
        challengeJson = request.json
        _require_mentor(challengeJson.get('created_by'))
```

- [ ] **Step 3: Call `_require_mentor` in `updateChallenge`** — right after the existing 404 check (`if not challengeUpdated or "ErrorMessage" in challengeUpdated: abort(404, ...)`):

```python
        _require_mentor(challengeJson.get('created_by'))
```

- [ ] **Step 4: Call `_require_mentor` in `deleteChallenge`** — this route reads `created_by` from `request.get_json(silent=True) or {}` already (see existing `deleteJson = request.get_json(silent=True) or {}` / `user_id = deleteJson.get('created_by')`); right after that, before the existing `is_creator` check, add:

```python
        _require_mentor(user_id)
```

- [ ] **Step 5: Compile-check**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && python3 -m py_compile src/views/view_challenges.py && echo OK"
```
Expected: `OK`

- [ ] **Step 6: Build and deploy backend**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && docker compose build backend && docker compose up -d backend"
```

- [ ] **Step 7: Verify on production** — a non-mentor (or unknown) `created_by` is rejected, a real Mentor succeeds:

```bash
ssh 91.200.121.128 'bash -s' <<"REMOTE"
TOKEN=$(curl -s https://thinkupacademy.ro/api/token | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "-- non-mentor tries to create a challenge (expect 403) --"
curl -s -o /dev/null -w "HTTP:%{http_code}\n" -X POST "https://thinkupacademy.ro/challenges/plan-test-c-x" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"x","description":"x","deadline":"2027-01-01T00:00:00","maxScore":100,"created_by":"nonexistent-user","creation_date":"2026-09-05"}'

echo "-- create a temporary real Mentor to test the happy path --"
MID="plan-test-mentor-$(date +%s)"
curl -s -o /dev/null -w "create mentor HTTP:%{http_code}\n" -X POST "https://thinkupacademy.ro/users/$MID" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d "{\"id\":\"$MID\",\"name\":\"Plan Test Mentor\",\"email\":\"plan.test@mentor.think-up.academy\",\"description\":\"x\"}"

echo "-- mentor creates a challenge (expect 200) --"
curl -s -o /dev/null -w "HTTP:%{http_code}\n" -X POST "https://thinkupacademy.ro/challenges/plan-test-c-y" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d "{\"name\":\"x\",\"description\":\"x\",\"deadline\":\"2027-01-01T00:00:00\",\"maxScore\":100,\"created_by\":\"$MID\",\"creation_date\":\"2026-09-05\"}"

echo "-- cleanup --"
curl -s -o /dev/null -w "delete challenge HTTP:%{http_code}\n" -X DELETE "https://thinkupacademy.ro/challenges/plan-test-c-y" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "{\"created_by\":\"$MID\"}"
curl -s -o /dev/null -w "delete mentor HTTP:%{http_code}\n" -X DELETE "https://thinkupacademy.ro/users/$MID" \
  -H "Authorization: Bearer $TOKEN"
REMOTE
```
Expected: first `HTTP:403`, mentor creation `200`, challenge creation `200`, both cleanup calls `200`.

- [ ] **Step 8: Commit**

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-backend/src/views/view_challenges.py && git commit -m "Restrictioneaza POST/PUT/DELETE /challenges la Mentori

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

### Task 2.2: Frontend — `useMyUser` exposes the logged-in user's `role`

**Files:**
- Modify: `platform-frontend/src/hooks/useMyUser.js`

**Interfaces:**
- Produces: the `User` object returned by `useMyUserContext()` now has a `role` field (`"Mentor"` or `"Student"`, whatever `GET /users/<id>` returns), usable anywhere in the frontend as `user.role`.

- [ ] **Step 1: Edit `getUserData` in `useMyUser.js`** — add `role` to the object passed to `setUser`:

```jsx
            setUser({
                name: response.data.name,
                email: response.data.email,
                description: response.data.description,
                picture: `${process.env.NEXT_PUBLIC_API_URL}/storage/thinkup-profile-picture/${response.data.profile_picture}${response.data.profile_picture_extension}`,
                cover_picture:`${process.env.NEXT_PUBLIC_API_URL}/storage/thinkup-user-cover-images/${response.data.cover_picture}${response.data.cover_picture_extension}`,
                social_connections:{
                    gitHub:response.data.social_connections?.gitHub,
                    twitter:response.data.social_connections?.twitter,
                    linkedin:response.data.social_connections?.linkedin,
                    instagram:response.data.social_connections?.instagram,
                    facebook:response.data.social_connections?.facebook,
                },
                id: User.id,
                role: response.data.role,
                settings: response.data.settings,
                perms: response.data.perms,
            });
```
(only the added `role: response.data.role,` line is new — everything else in this object stays exactly as-is.)

- [ ] **Step 2: Build check**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-frontend && docker exec thinkup-frontend npm run build 2>&1 | tail -20"
```
Expected: build completes, no new errors.

- [ ] **Step 3: Commit** (deploy together with Task 2.3, same feature)

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-frontend/src/hooks/useMyUser.js && git commit -m "useMyUser expune role-ul userului logat

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

### Task 2.3: Frontend — Challenges admin page (list, create, edit, delete)

**Files:**
- Create: `platform-frontend/src/pages/Challenges/index.js`
- Create: `platform-frontend/styles/Challenges.module.css`

**Interfaces:**
- Consumes: `user.role` (Task 2.2), `GET/POST/PUT/DELETE /challenges` (existing route, now Mentor-restricted per Task 2.1), `apiClient` from `../../utils/apiClient`, `useMyUserContext` from `../../contexts/UserContext`.

- [ ] **Step 1: Create `platform-frontend/styles/Challenges.module.css`**:

```css
.ChallengesPage {
    padding: 2rem;
    max-width: 700px;
    margin: 0 auto;
}

.ChallengeRow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-radius: 0.5rem;
    background: var(--color-background-secondary, #f4f4f4);
    margin-bottom: 0.75rem;
}

.ChallengeRow h3 {
    margin: 0 0 0.25rem 0;
}

.ChallengeActions button {
    margin-left: 0.5rem;
}

.ChallengeForm {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 2rem;
}

.ChallengeForm input,
.ChallengeForm textarea {
    padding: 0.5rem;
    border-radius: 0.375rem;
    border: 1px solid #ccc;
}

.NoAccess {
    padding: 2rem;
    text-align: center;
}
```

- [ ] **Step 2: Create `platform-frontend/src/pages/Challenges/index.js`**:

```jsx
import React, { useState, useEffect } from "react";
import styles from "../../../styles/Challenges.module.css";
import apiClient from "../../utils/apiClient";
import { useMyUserContext } from "../../contexts/UserContext";
import ScrollContainer from "../../components/Containers/ScrollContainer";

const emptyForm = {
    id: "",
    name: "",
    description: "",
    deadline: "",
    maxScore: 100,
};

const ChallengesPage = () => {
    const user = useMyUserContext();
    const [Challenges, setChallenges] = useState([]);
    const [Form, setForm] = useState(emptyForm);
    const [EditingId, setEditingId] = useState(null);
    const [Error, setError] = useState("");

    const loadChallenges = async () => {
        try {
            const response = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges`
            );
            setChallenges(response.data.challenges || []);
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {
        loadChallenges();
    }, []);

    if (user === undefined) {
        return (
            <ScrollContainer>
                <p className={styles.NoAccess}>Se încarcă...</p>
            </ScrollContainer>
        );
    }

    if (user.role !== "Mentor") {
        return (
            <ScrollContainer>
                <p className={styles.NoAccess}>
                    Doar mentorii pot gestiona challenge-urile.
                </p>
            </ScrollContainer>
        );
    }

    const startEdit = (challenge) => {
        setEditingId(challenge.id);
        setForm({
            id: challenge.id,
            name: challenge.name,
            description: challenge.description,
            deadline: challenge.deadline,
            maxScore: challenge.maxScore,
        });
    };

    const resetForm = () => {
        setEditingId(null);
        setForm(emptyForm);
        setError("");
    };

    const submitForm = async () => {
        if (!Form.id || !Form.name || !Form.deadline) {
            setError("Id, nume și deadline sunt obligatorii.");
            return;
        }
        setError("");
        try {
            if (EditingId) {
                await apiClient.put(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges/${EditingId}`,
                    {
                        name: Form.name,
                        description: Form.description,
                        deadline: Form.deadline,
                        maxScore: Number(Form.maxScore),
                        created_by: user.id,
                    }
                );
            } else {
                await apiClient.post(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges/${Form.id}`,
                    {
                        name: Form.name,
                        description: Form.description,
                        deadline: Form.deadline,
                        maxScore: Number(Form.maxScore),
                        created_by: user.id,
                        creation_date: new Date().toISOString(),
                    }
                );
            }
            resetForm();
            await loadChallenges();
        } catch (err) {
            console.log(err);
            setError(
                err.response?.data?.error || "A apărut o eroare la salvare."
            );
        }
    };

    const deleteChallenge = async (id) => {
        try {
            await apiClient.delete(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges/${id}`,
                { data: { created_by: user.id } }
            );
            await loadChallenges();
        } catch (err) {
            console.log(err);
            setError(
                err.response?.data?.error || "A apărut o eroare la ștergere."
            );
        }
    };

    return (
        <ScrollContainer className={styles.ChallengesPage}>
            <h1>Challenges</h1>

            <div className={styles.ChallengeForm}>
                <h3>{EditingId ? "Editează challenge" : "Challenge nou"}</h3>
                {!EditingId && (
                    <input
                        placeholder="id (ex: challenge-1)"
                        value={Form.id}
                        onChange={(e) =>
                            setForm({ ...Form, id: e.target.value })
                        }
                    />
                )}
                <input
                    placeholder="Nume (ex: Challenge 1)"
                    value={Form.name}
                    onChange={(e) => setForm({ ...Form, name: e.target.value })}
                />
                <textarea
                    placeholder="Descriere"
                    value={Form.description}
                    onChange={(e) =>
                        setForm({ ...Form, description: e.target.value })
                    }
                />
                <input
                    type="datetime-local"
                    value={Form.deadline}
                    onChange={(e) =>
                        setForm({ ...Form, deadline: e.target.value })
                    }
                />
                <input
                    type="number"
                    placeholder="Scor maxim"
                    value={Form.maxScore}
                    onChange={(e) =>
                        setForm({ ...Form, maxScore: e.target.value })
                    }
                />
                {Error && <p style={{ color: "red" }}>{Error}</p>}
                <div>
                    <button onClick={submitForm}>
                        {EditingId ? "Salvează" : "Creează"}
                    </button>
                    {EditingId && (
                        <button onClick={resetForm}>Anulează</button>
                    )}
                </div>
            </div>

            {Challenges.map((challenge) => (
                <div key={challenge.id} className={styles.ChallengeRow}>
                    <div>
                        <h3>{challenge.name}</h3>
                        <p>{challenge.description}</p>
                        <p>
                            Deadline: {challenge.deadline} · Scor max:{" "}
                            {challenge.maxScore}
                        </p>
                    </div>
                    <div className={styles.ChallengeActions}>
                        <button onClick={() => startEdit(challenge)}>
                            Editează
                        </button>
                        <button onClick={() => deleteChallenge(challenge.id)}>
                            Șterge
                        </button>
                    </div>
                </div>
            ))}
        </ScrollContainer>
    );
};

export default ChallengesPage;
```

- [ ] **Step 3: Build check**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-frontend && docker exec thinkup-frontend npm run build 2>&1 | tail -30"
```
Expected: `/Challenges` listed in the route table, build completes with no new errors.

- [ ] **Step 4: Deploy frontend**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && docker compose build frontend && docker compose up -d frontend"
```

- [ ] **Step 5: Verify on production, and seed the 4 real permanent Challenges** — this is also where the real, permanent "Challenge 1..4" rows get created (not deleted after — this is production data, per the approved design):

```bash
ssh 91.200.121.128 'bash -s' <<"REMOTE"
TOKEN=$(curl -s https://thinkupacademy.ro/api/token | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
OWNER="108725634211690813513"

for i in 1 2 3 4; do
  echo "-- create Challenge $i --"
  curl -s -o /dev/null -w "HTTP:%{http_code}\n" -X POST "https://thinkupacademy.ro/challenges/challenge-$i" \
    -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
    -d "{\"name\":\"Challenge $i\",\"description\":\"Challenge $i\",\"deadline\":\"2027-06-01T00:00:00\",\"maxScore\":100,\"created_by\":\"$OWNER\",\"creation_date\":\"2026-09-05\"}"
done

echo "-- confirm all 4 exist --"
curl -s "https://thinkupacademy.ro/challenges" | python3 -c "import sys,json; d=json.load(sys.stdin); print([c['name'] for c in d['challenges']])"
REMOTE
```
Expected: 4× `HTTP:200`, final list prints `['Challenge 1', 'Challenge 2', 'Challenge 3', 'Challenge 4']` (order may vary).

**Note:** this step requires `108725634211690813513` to have `role: 'Mentor'` in the DB for the `_require_mentor` check from Task 2.1 to pass. Check first with `docker exec thinkup-app python3 -c "..."` reading the `Users` table; if that user is a Student, either ask the user which real Mentor account to use, or (with the user's explicit go-ahead) temporarily use a throwaway Mentor account created the same way as Task 2.1 Step 7, then delete it after seeding.

- [ ] **Step 6: Migrate the 2 real existing projects to Challenge 1** (per the approved design — do this only after Step 5 confirms `challenge-1` exists):

```bash
ssh 91.200.121.128 "docker exec thinkup-app python3 -c \"
import boto3
db = boto3.resource('dynamodb', endpoint_url='http://scylladb:8000', region_name='eu-central-1', aws_access_key_id='local', aws_secret_access_key='local')
table = db.Table('Projects')
for pid in ['mtega0tmtzvbkcudjoh', 'mtmntkh9asjptglks8']:
    table.update_item(Key={'id': pid}, UpdateExpression='SET challengeId = :c REMOVE areaOfImplementation', ExpressionAttributeValues={':c': 'challenge-1'})
    print(pid, 'migrated')
\""
```
Expected: both ids print `migrated`. Then verify: `curl -s https://thinkupacademy.ro/projects/mtega0tmtzvbkcudjoh | python3 -c "import sys,json; print(json.load(sys.stdin)['challengeId'])"` prints `challenge-1`.

- [ ] **Step 7: Commit**

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-frontend/src/pages/Challenges/index.js platform-frontend/styles/Challenges.module.css && git commit -m "Adauga pagina admin pentru Challenges (CRUD, restrictionat la Mentori)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

## Piece 3 — Notare pe proiect (parallel-eligible after Piece 1 checkpoint)

### Task 3.1: Backend — `Submission` gains `projectId`, new project-based grading route

**Files:**
- Modify: `platform-backend/src/model/entity/submission.py`
- Modify: `platform-backend/src/model/entity/jsonencoders/submission_encoder.py`
- Modify: `platform-backend/src/views/view_submissions.py`

**Interfaces:**
- Consumes: `apiProjects` pattern — this view doesn't currently import project access; add `from dynamoDB import setup` (already imported) and reuse `setup.startSetup('Projects')` directly (matches how `dbCrudUsers`/`dbCrudSubmissions` are already wired in this file — no need for the full `API_CRUD_PROJECTS` class, just the raw `getProject` DB call).
- Produces: `POST /submissions/project/<projectId>` (body: `mentorId`, `score`, `feedback` optional) — creates/updates one `Submission` per entry in the project's `adminList`, each with the new `projectId` field.

- [ ] **Step 1: Edit `submission.py`** — add `projectId` to the constructor:

```python
import string


class Submission:
    def __init__(self, id: str, studentId: str, challengeId: str, score, gradedBy: str, gradedDate, feedback: string = None, projectId: string = None):
        self.__id = id
        self.__studentId = studentId
        self.__challengeId = challengeId
        self.__score = score
        self.__gradedBy = gradedBy
        self.__gradedDate = gradedDate
        self.__feedback = feedback
        self.__projectId = projectId
```

Add, alongside the other getters:
```python
    def get_projectId(self):
        return self.__projectId

    def set_projectId(self, projectId: string):
        self.__projectId = projectId
```

- [ ] **Step 2: Edit `submission_encoder.py`** — add `projectId` to the emitted dict:

```python
class SubmissionEncoder():
  def toJSON(o):
    if isinstance(o, Submission):
      Item = {
        'id': o.get_id(),
        'studentId': o.get_studentId(),
        'challengeId': o.get_challengeId(),
        'score': o.get_score(),
        'gradedBy': o.get_gradedBy(),
        'gradedDate': o.get_gradedDate(),
        'feedback': o.get_feedback(),
        'projectId': o.get_projectId(),
      }
      return Item
    return None
```

- [ ] **Step 3: Add the project-based grading route to `view_submissions.py`** — add a `Projects` table reference near the top (alongside the existing `dbCrudSubmissions`/`dbCrudUsers`):

```python
dbCrudProjects = setup.startSetup('Projects')
```

Add a new route, placed after `gradeSubmission`:

```python
@urlSubmissions.route('/submissions/project/<string:project_id>', methods=['POST'])
@require_auth()
def gradeProject(project_id: str):
    """Grade every admin of a project for the project's challenge

    Body:
        mentorId (str): id of the mentor granting the score (must resolve to a Mentor user)
        score (number): the score granted
        feedback (str, optional): free-text feedback

    Args:
        project_id (str): id of the project being graded

    Returns:
        _type_: response
    """
    try:
        gradeJson = request.json
        if not gradeJson:
            abort(400, description="Missing JSON body")

        mentor_id = gradeJson.get('mentorId')
        if not mentor_id:
            abort(400, description="mentorId is required")

        mentor = dbCrudUsers.getUser(mentor_id)
        if not mentor or "ErrorMessage" in mentor:
            logger.warning(f"Grading attempt by unknown user {mentor_id}")
            abort(403, description="You are not authorized to grade submissions")

        if mentor.get('role') != 'Mentor':
            logger.warning(f"Grading attempt by non-mentor user {mentor_id} (role={mentor.get('role')})")
            abort(403, description="Only mentors can grade submissions")

        project = dbCrudProjects.getProject(project_id)
        if not project or "ErrorMessage" in project:
            abort(404, description="Project not found")

        challenge_id = project.get('challengeId')
        if not challenge_id:
            abort(400, description="This project has no challenge assigned")

        score = Decimal(str(gradeJson['score']))
        feedback = gradeJson.get('feedback')
        gradedDate = datetime.now().isoformat()

        results = []
        for admin_id in project.get('adminList', []):
            submission_id = f"{challenge_id}#{admin_id}"
            submissionObj = Submission(submission_id, admin_id, challenge_id, score, mentor_id, gradedDate, feedback, project_id)
            submissionDict = SubmissionEncoder.toJSON(submissionObj)

            existing = dbCrudSubmissions.getSubmission(submission_id)
            if "ErrorMessage" in existing:
                result = dbCrudSubmissions.addSubmission(submissionDict)
            else:
                result = dbCrudSubmissions.updateSubmission(submissionDict)
            results.append(_serializable(submissionDict))

        logger.info(f"Project {project_id} graded by mentor {mentor_id}, {len(results)} submission(s)")
        return jsonify({"submissions": results})
    except KeyError as e:
        logger.warning(f"Missing field grading project {project_id}: {e}")
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error grading project {project_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
```

- [ ] **Step 4: Compile-check**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && python3 -m py_compile src/model/entity/submission.py src/model/entity/jsonencoders/submission_encoder.py src/views/view_submissions.py && echo OK"
```
Expected: `OK`

- [ ] **Step 5: Build and deploy backend**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && docker compose build backend && docker compose up -d backend"
```

- [ ] **Step 6: Verify on production** — grade a throwaway project with 2 admins, confirm 2 `Submission`s created, both with the right `projectId`:

```bash
ssh 91.200.121.128 'bash -s' <<"REMOTE"
TOKEN=$(curl -s https://thinkupacademy.ro/api/token | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
OWNER="108725634211690813513"
TS=$(date +%s)
PID="plan-test-grade-project-$TS"

echo "-- create a test project on challenge-1, then add a second admin directly (simulates a team) --"
curl -s -o /dev/null -w "create project HTTP:%{http_code}\n" -X POST "https://thinkupacademy.ro/projects/$PID" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d "{\"id\":\"$PID\",\"name\":\"Grading test\",\"challengeId\":\"challenge-1\",\"creation_date\":\"05/9/2026\",\"description\":\"x\",\"created_by\":\"$OWNER\"}"

docker exec thinkup-app python3 -c "
import boto3
db = boto3.resource('dynamodb', endpoint_url='http://scylladb:8000', region_name='eu-central-1', aws_access_key_id='local', aws_secret_access_key='local')
table = db.Table('Projects')
table.update_item(Key={'id': '$PID'}, UpdateExpression='SET adminList = :a', ExpressionAttributeValues={':a': ['$OWNER', '113528018155821801130']})
print('added second admin')
"

echo "-- mentor grades the project (expect 200, 2 submissions returned) --"
curl -s "https://thinkupacademy.ro/submissions/project/$PID" -X POST \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d "{\"mentorId\":\"$OWNER\",\"score\":90,\"feedback\":\"Great teamwork\"}" | python3 -m json.tool

echo "-- cleanup: delete the 2 submissions, the test project, restore challengeId isn't needed (test project deleted) --"
docker exec thinkup-app python3 -c "
import boto3
db = boto3.resource('dynamodb', endpoint_url='http://scylladb:8000', region_name='eu-central-1', aws_access_key_id='local', aws_secret_access_key='local')
db.Table('Submissions').delete_item(Key={'id': 'challenge-1#$OWNER'})
db.Table('Submissions').delete_item(Key={'id': 'challenge-1#113528018155821801130'})
print('submissions deleted')
"
curl -s -o /dev/null -w "delete project HTTP:%{http_code}\n" -X DELETE "https://thinkupacademy.ro/projects/$PID" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "{\"created_by\":\"$OWNER\"}"
REMOTE
```
**Warning for whoever executes this:** grading `challenge-1` here temporarily writes a real `Submission` row keyed `challenge-1#108725634211690813513` and `challenge-1#113528018155821801130` — if either of those real users already has a real grade on `challenge-1` when this step runs, this test would silently overwrite it (same key). Check first with `GET /submissions/student/<id>` for both users; if either already has a `challenge-1` submission, use a different throwaway challenge id (seeded and deleted the same way as Task 1.2 Step 6) instead of the real `challenge-1`.

Expected: create `HTTP:200`, grading response is JSON with a `submissions` array of length 2, both entries have `projectId` == the test project id, cleanup succeeds.

- [ ] **Step 7: Commit**

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-backend/src/model/entity/submission.py platform-backend/src/model/entity/jsonencoders/submission_encoder.py platform-backend/src/views/view_submissions.py && git commit -m "Submission capata projectId, ruta noua de notare pe proiect (echipa)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

### Task 3.2: Frontend — mentor grading page

**Files:**
- Create: `platform-frontend/src/pages/Challenges/[id]/grade.js`
- Create: `platform-frontend/styles/GradeChallenge.module.css`

**Interfaces:**
- Consumes: `user.role` (Task 2.2), `GET /challenges/<id>` (existing), a new-to-this-page way to list projects for a challenge — **no existing route filters projects by `challengeId`**, so this page fetches `GET /projects` (existing, returns all projects) and filters client-side by `challengeId` (small dataset, matches how `get_all_challenges`/`get_all_projects` are already used elsewhere without pagination). `POST /submissions/project/<projectId>` (Task 3.1).

- [ ] **Step 1: Create `platform-frontend/styles/GradeChallenge.module.css`**:

```css
.GradePage {
    padding: 2rem;
    max-width: 700px;
    margin: 0 auto;
}

.ProjectRow {
    padding: 1rem;
    border-radius: 0.5rem;
    background: var(--color-background-secondary, #f4f4f4);
    margin-bottom: 0.75rem;
}

.ProjectRow h3 {
    margin: 0 0 0.5rem 0;
}

.GradeForm {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.GradeForm input {
    padding: 0.4rem;
    border-radius: 0.375rem;
    border: 1px solid #ccc;
}

.NoAccess {
    padding: 2rem;
    text-align: center;
}
```

- [ ] **Step 2: Create `platform-frontend/src/pages/Challenges/[id]/grade.js`**:

```jsx
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import styles from "../../../../styles/GradeChallenge.module.css";
import apiClient from "../../../utils/apiClient";
import { useMyUserContext } from "../../../contexts/UserContext";
import ScrollContainer from "../../../components/Containers/ScrollContainer";

const GradeChallengePage = () => {
    const router = useRouter();
    const { id } = router.query;
    const user = useMyUserContext();
    const [Challenge, setChallenge] = useState(null);
    const [Projects, setProjects] = useState([]);
    const [Scores, setScores] = useState({});
    const [Feedbacks, setFeedbacks] = useState({});
    const [Status, setStatus] = useState({});

    const loadData = async () => {
        if (!id) return;
        try {
            const challengeResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges/${id}`
            );
            setChallenge(challengeResponse.data);

            const projectsResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/projects`
            );
            const allProjects = projectsResponse.data.projects || [];
            setProjects(allProjects.filter((p) => p.challengeId === id));
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {
        loadData();
    }, [id]);

    if (user === undefined) {
        return (
            <ScrollContainer>
                <p className={styles.NoAccess}>Se încarcă...</p>
            </ScrollContainer>
        );
    }

    if (user.role !== "Mentor") {
        return (
            <ScrollContainer>
                <p className={styles.NoAccess}>
                    Doar mentorii pot nota proiecte.
                </p>
            </ScrollContainer>
        );
    }

    const gradeProject = async (projectId) => {
        const score = Scores[projectId];
        if (score === undefined || score === "") {
            setStatus({ ...Status, [projectId]: "Introdu un scor." });
            return;
        }
        try {
            await apiClient.post(
                `${process.env.NEXT_PUBLIC_API_URL}/submissions/project/${projectId}`,
                {
                    mentorId: user.id,
                    score: Number(score),
                    feedback: Feedbacks[projectId] || "",
                }
            );
            setStatus({ ...Status, [projectId]: "Notat cu succes." });
        } catch (err) {
            console.log(err);
            setStatus({
                ...Status,
                [projectId]:
                    err.response?.data?.error || "A apărut o eroare la notare.",
            });
        }
    };

    return (
        <ScrollContainer className={styles.GradePage}>
            <h1>{Challenge ? Challenge.name : "Challenge"}</h1>
            <p>{Challenge ? Challenge.description : ""}</p>

            {Projects.length === 0 && (
                <p>Niciun proiect pe acest challenge încă.</p>
            )}

            {Projects.map((project) => (
                <div key={project.id} className={styles.ProjectRow}>
                    <h3>{project.name}</h3>
                    <p>{project.description}</p>
                    <div className={styles.GradeForm}>
                        <input
                            type="number"
                            placeholder="Scor"
                            value={Scores[project.id] || ""}
                            onChange={(e) =>
                                setScores({
                                    ...Scores,
                                    [project.id]: e.target.value,
                                })
                            }
                        />
                        <input
                            type="text"
                            placeholder="Feedback (opțional)"
                            value={Feedbacks[project.id] || ""}
                            onChange={(e) =>
                                setFeedbacks({
                                    ...Feedbacks,
                                    [project.id]: e.target.value,
                                })
                            }
                        />
                        <button onClick={() => gradeProject(project.id)}>
                            Notează
                        </button>
                    </div>
                    {Status[project.id] && <p>{Status[project.id]}</p>}
                </div>
            ))}
        </ScrollContainer>
    );
};

export default GradeChallengePage;
```

- [ ] **Step 3: Build check**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-frontend && docker exec thinkup-frontend npm run build 2>&1 | tail -30"
```
Expected: `/Challenges/[id]/grade` listed in the route table, no new errors.

- [ ] **Step 4: Deploy frontend**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && docker compose build frontend && docker compose up -d frontend"
```

- [ ] **Step 5: Verify on production** — confirm the page's underlying API calls work end-to-end using the same throwaway-project pattern as Task 3.1 Step 6 (create test project on a throwaway challenge, confirm it would appear in the `GET /projects` filtered list, grade it via `POST /submissions/project/<id>`, clean up). Since there's no browser automation available in this environment by default, this step verifies the API contract the page depends on, not pixels — note that explicitly when reporting results, and if browser tools are available in this session, additionally load `/Challenges/<id>/grade` and confirm it renders the project + grade form.

- [ ] **Step 6: Commit**

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add "platform-frontend/src/pages/Challenges/[id]/grade.js" platform-frontend/styles/GradeChallenge.module.css && git commit -m "Adauga pagina de notare pe proiect pentru mentori

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

## Piece 4 — `DeadlineBanner` reflects participation via project (parallel-eligible after Piece 1 checkpoint)

### Task 4.1: Frontend — "not yet participating" checks for a Project, not a Submission

**Files:**
- Modify: `platform-frontend/src/components/Cards/DeadlineBanner.js`

**Interfaces:**
- Consumes: `GET /user_projects/<id>` (existing route, returns `{"projects": [...]}` of projects the user owns/administers — confirmed via `api_crud_projects.py::getOwnedProjects`), replacing the existing `GET /submissions/student/<id>` call.

- [ ] **Step 1: Edit `getDeadlineData` in `DeadlineBanner.js`** — replace the submissions fetch with a project-ownership fetch, and switch the "already participating" check to `challengeId`:

```jsx
    const getDeadlineData = async () => {
        if (!props.user_id) {
            setBanners([]);
            return;
        }
        try {
            const challengesResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges`
            );
            const projectsResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/user_projects/${props.user_id}`
            );

            const challenges = challengesResponse.data.challenges || [];
            const projects = projectsResponse.data.projects || [];
            const participatingChallengeIds = new Set(
                projects.map((project) => project.challengeId)
            );

            const now = Date.now();

            const upcoming = challenges
                .filter(
                    (challenge) =>
                        !participatingChallengeIds.has(challenge.id)
                )
                .map((challenge) => ({
                    ...challenge,
                    msRemaining: new Date(challenge.deadline).getTime() - now,
                }))
                .filter(
                    (challenge) =>
                        !Number.isNaN(challenge.msRemaining) &&
                        challenge.msRemaining > 0 &&
                        challenge.msRemaining < HOURS_48_MS
                );

            setBanners(upcoming);
        } catch (err) {
            console.log(err);
            setBanners([]);
        }
    };
```
(only the two `apiClient.get` calls and the `participatingChallengeIds` variable name/derivation change — the rest of the function body, including the final `.filter`, stays identical.)

- [ ] **Step 2: Build check**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-frontend && docker exec thinkup-frontend npm run build 2>&1 | tail -20"
```
Expected: build completes, no new errors.

- [ ] **Step 3: Deploy frontend**

```bash
ssh 91.200.121.128 "cd /root/thinkup/platform-backend && docker compose build frontend && docker compose up -d frontend"
```

- [ ] **Step 4: Verify on production** — a user with a project on `challenge-1` (e.g. `108725634211690813513`, after Piece 2's migration) does not see a banner for `challenge-1` even with a near deadline; a user with no project on any challenge does see one if a challenge's deadline is within 48h. Since `challenge-1`'s deadline is seeded far in the future (`2027-06-01`) in Task 2.3 Step 5, this step temporarily edits that one challenge's deadline to confirm the logic, then restores it:

```bash
ssh 91.200.121.128 'bash -s' <<"REMOTE"
TOKEN=$(curl -s https://thinkupacademy.ro/api/token | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
OWNER="108725634211690813513"

echo "-- temporarily set challenge-1 deadline to 24h from now --"
NEAR=$(python3 -c "from datetime import datetime, timedelta; print((datetime.now() + timedelta(hours=24)).isoformat())")
curl -s -o /dev/null -w "HTTP:%{http_code}\n" -X PUT "https://thinkupacademy.ro/challenges/challenge-1" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d "{\"deadline\":\"$NEAR\",\"created_by\":\"$OWNER\"}"

echo "-- confirm the API contract the banner relies on: owner has a project on challenge-1 --"
curl -s "https://thinkupacademy.ro/user_projects/$OWNER" | python3 -c "import sys,json; d=json.load(sys.stdin); print([p['challengeId'] for p in d['projects']])"

echo "-- restore challenge-1 deadline --"
curl -s -o /dev/null -w "HTTP:%{http_code}\n" -X PUT "https://thinkupacademy.ro/challenges/challenge-1" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d "{\"deadline\":\"2027-06-01T00:00:00\",\"created_by\":\"$OWNER\"}"
REMOTE
```
Expected: both `PUT` calls `200`, project list for `$OWNER` includes `"challenge-1"` (confirming `participatingChallengeIds` would exclude it from the banner). If browser tools are available, additionally load the homepage as that user and visually confirm no banner appears for Challenge 1.

- [ ] **Step 5: Commit**

```bash
ssh 91.200.121.128 'cd /root/thinkup && git add platform-frontend/src/components/Cards/DeadlineBanner.js && git commit -m "DeadlineBanner verifica participarea prin proiect, nu prin notare

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: <session-url>"'
```

---

## Final checkpoint (after all 4 pieces land)

- [ ] `docker ps` on the VPS shows `thinkup-app` and `thinkup-frontend` both `Up` and freshly restarted.
- [ ] `git log --oneline -12` shows all commits from this plan.
- [ ] No leftover `plan-test-*` ids in `Projects`, `Challenges`, `Submissions`, or `Users` tables (re-run the scan pattern used throughout this plan and in prior sessions).
- [ ] Run backend build once more (`docker compose build backend`) and frontend `npm run lint && npm run build` inside `thinkup-frontend`, confirm no new errors beyond the pre-existing `<img>`/hook-dependency warnings already present before this plan.
- [ ] Report to the user, piece by piece, exactly like every prior fix on this VPS: what changed, how it was tested, what's left clean.
